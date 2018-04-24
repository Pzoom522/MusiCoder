#-*- coding: UTF-8 -*-
import socket,time,struct,os,sys,threading,backend_run
import hashlib
import time

def log(ip,message):
    #1. format time-ip-message
    #2. log to a file 
    pass
class Server:
    def __init__(self,socket):
        self.socket=socket
        self.packet='4s128sq' #define the file head format
        self.sendf='send'     #sending file flag 
        self.convertf='conv'  #converting flag 

    def sendFile(self,connection,filepath):    
        if os.path.isfile(filepath):

            #1. Pack file head info. 
            fileinfo_size=struct.calcsize(self.packet) 
            fhead = struct.pack(self.packet,self.sendf.encode(),os.path.basename(filepath).encode(),os.stat(filepath).st_size)
            #2. Send file head.
            connection.sendall(fhead) 
            
            #3. Send the file content. 
            fo = open(filepath,'rb')
            while True:
                filedata = fo.read(1024)
                if not filedata:
                    break
                connection.sendall(filedata)
            fo.close()

            #4. Return True if all went well.
            return True
        else:

            print("File not exists")
            
            #5. Return False if file not exists.
            return False
            
    def receive_thread(self,connection,address): 
        while True:
            try:
                #1. Recv filehead pack ,we need to know how long the file is and some other infos.
                fileinfo_size=struct.calcsize(self.packet) 
                buf = connection.recv(fileinfo_size)
                if buf:  #I don`t acutually understand when recv will return 0 

                    #2. Extract info from the pack.
                    #   Use unpack and bytes.decode
                    #Notice: a pack is padded with zeros'\x00', we need to strip it off.
                    #   filename is the last element in the pack, so we do that for it.
                    flag,filename,filesize =struct.unpack(self.packet,buf)    
                    flag=flag.decode('ascii')
                    filename=filename.decode('ascii')
                    filename=filename.strip('\x00')
                    

                    if flag==self.sendf:

                        #3. Rename the file with sha-256 to prevent filename collision.
                        sha=hashlib.sha1()
                        sha.update(str(time.clock()).encode())
                        _,ext=os.path.splitext(filename)
                        filename=sha.hexdigest()[:10]+ext

                        #4. recv it with filename generated .       
                        filepath = os.path.join('receive',filename) 
                        file = open(filepath,'wb')
                        recvd_size = 0

                        print ('stat receiving...')
                        while not recvd_size == filesize:
                            if filesize - recvd_size > 1024:
                                rdata = connection.recv(1024)
                                recvd_size += len(rdata)
                            else:
                                rdata = connection.recv(filesize - recvd_size) 
                                recvd_size += len(rdata)
                            file.write(rdata)

                        file.close()
                        
                        #5. Initiate a converting task and send the img.
                        task=backend_run.task(filepath) 
                        task.soundToImage()
                        self.sendFile(connection,task.endecoder.content_img_path)
                        
                        #6. Remove all temp files
                        os.remove(filepath)

                        print('transfering done')
                    elif flag==self.convertf:

                        #6. If this a instruction , do the converting work.

                        style,quality=filename.split('.')

                        print (style,quality)
                        print ('start converting')

                        task.convert(style)
                        print ("doing GLA..") 
                        task.imageToSound(quality,style)
                        print('convert done') 

                        self.sendFile(connection,task.endecoder.trans_img_path)
                        self.sendFile(connection,task.endecoder.trans_audio_path)

                        #7. Remove all temp files
                        os.remove(task.endecoder.content_img_path)
                        os.remove(task.endecoder.trans_img_path)
                        os.remove(task.endecoder.trans_audio_path)
                        print('send done')
                else:
                    #If buf is null, we can say the remote has shutdown
                    raise Exception("Connection closed by peer")
            except Exception as ex:
                print(ex)
                print("process error")
                connection.close()
                return 
                        

    def listen(self,maxClients):
        #1. Listeing for connection. The maximal of clients waiting for connection is defined by maxClients
        self.socket.listen(maxClients)
        connection=None
        while True:
            try:
                connection,address=self.socket.accept()
                #2. Set the keep alive protocol, which will try to ping client after serveral seconds of silence.
           
                connection.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)  #enable the protocol
                connection.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 3) 
                connection.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 1)
                connection.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 3)
                print('Connected by ',address)

                #3. Start a serving thread for the client.
                thread = threading.Thread(target=self.receive_thread,args=(connection,address)) 
                thread.start()
            except KeyboardInterrupt as it:          

                #4. Ctrl+C to exit      
                 self.socket.close()
                 print ("Exit")
                 break          

def bind(ip,port):
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
        s.bind((ip,port)) 

        return Server(s)  
    
def main(args):
    port=int(args[1])%65535 #set the port use sys argv 
    server=bind('0.0.0.0',port)     #0.0.0.0 refers to this host itself
    server.listen(5)

if __name__ == '__main__':
    main(sys.argv)
