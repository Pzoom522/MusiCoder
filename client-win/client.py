# -*- coding:UTF-8 -*-
import socket,os,struct
import thread
import paramiko
import time
import sys
import gui
class Client:
    def __init__(self,socket):
        self.socket=socket   
        self.packet='4s128sq'#define filehead format
        self.sendf='send'    #sending-file flag
        self.convertf='conv' #converting flag
                             #Flag will be used in packect head , defines the type of packet.
                             #Remember there are two kinds of packes, filehead packet and instruction packet.
                             
        self.trigger=None    #call back function which is triggered when a file is received
        self.error_trig=None #call back function which is triggered when errors happened
    def sendSound(self,filepath):    
        if os.path.isfile(filepath):
    
            #1. Pack file head info.
            fhead = struct.pack(self.packet,self.sendf,os.path.basename(filepath),os.stat(filepath).st_size)
            print fhead

            #2. Send file head.
            self.socket.sendall(fhead) 
          
            #3. Send the file content. 
            fo = open(filepath,'rb')
            while True:
                filedata = fo.read(1024)
                if not filedata:
                    break
                self.socket.sendall(filedata)
            fo.close()

            #4. Return True if all went well.
            return True
        else:

            print("File not exists")
            #5. Return False if file not exists.
            return False
            
    def convert(self,style,quality):
        print 'convert',style+' '+quality

        # Pack instruction info , use dot to seperate style and quality strings.
        instr=struct.pack(self.packet,self.convertf,style+'.'+quality,0)
        self.socket.send(instr)
    def listen(self):

        #1. Create a temp directory to store files.
        if not os.path.exists('temp'):
            os.mkdir('temp')

        #2. Start listening thread.    
        thread.start_new_thread(self.receive_thread,(self.socket,None))
    def fileRecv(self,func):
        #set a call-back function , it will be called after receiving a file 
        self.trigger=func

    def connectFail(self,func):
        #set a call-back function  with no param, it will be called when connection is failed
        self.error_trig = func

    def receive_thread(self,connection,address):
          while True:
            try:
                #1. Recv filehead pack ,we need to know how long the file is and some other infos.
                fileinfo_size=struct.calcsize(self.packet) 
                buf = connection.recv(fileinfo_size)
                if buf: 

                    flag,filename,filesize =struct.unpack(self.packet,buf) 
                    #2. Extract info from the pack.
                    #   Use unpack and bytes.decode
                    #Notice:a. A pack is padded with zeros'\x00', we need to strip it off.
                    #   filename is the last element in the pack, so we do that for it.
                    #       b. Because this is client, so it is supposed to only receive sending-file flag

                    #3. Flag should be sendf, otherwise something is wrong.

                    if flag!=self.sendf:
                        raise Exception("Packet is not a filehead")

                    #4. Strip zeros and set a filepath to recv file.
                    filename = filename.strip('\00')
                    filepath = os.path.join('temp',filename)
                    
                    #5. Receive the file.
                    recvd_size = 0 
                    file = open(filepath,'wb')
                    print 'stat receiving...'
                    while not recvd_size == filesize:
                        if filesize - recvd_size > 1024:
                            rdata = connection.recv(1024)
                            recvd_size += len(rdata)
                        else:
                            rdata = connection.recv(filesize - recvd_size) 
                            recvd_size += len(rdata)
                        file.write(rdata)
                    file.close()
         
                    print 'receive done'

                    #6. Store the filepath and tigger the file_recv function.
                    self.filepath=filepath
                    if self.trigger:
                         self.trigger.emit()
                
            except Exception,ex:
                #7. Exception processing: close the conenction and trigger connection_fail function.
                print 'connection error'
                print ex
                connection.close()      #close and emit error
                self.error_trig.emit()
                return

def connect(ip,port):
    # 1. Initiate a socket.
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    #2. Set the keep alive protocol, which will try to ping client after serveral seconds of silence.
    s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    s.ioctl(socket.SIO_KEEPALIVE_VALS, (1, 1000, 500))
    
    #3. Connect server with a timeout of 4 seconds.
    s.settimeout(4)
    s.connect((ip,port))
    s.settimeout(None) #Disable timeout by setting it None

    return Client(s)      

def recvFile():
    print "Recv!"

if __name__ == '__main__':
    # This is a test function, which allows you to use the server without a GUI. 
    # Notice:this is only used in testing and not well-impelemented.
    port=0
    if len(sys.argv)==1:
        port=5050                         #Default port is 5050
    else:
        port=int(sys.argv[1])%65536       #Set port with sys.argv limited between 0 and 65535
    client=connect('140.143.62.99',port) #Notice:Modify this ip before you use it.
    client.listen()                       #Set up a listener for the coming files.
    client.fileRecv(recvFile)
    #
    while True:
        filepath=input('Please input music path')
        if os.path.isfile(filepath) and filepath.endswith(('.mp3','.wav')) :
            client.sendSound(filepath)
            client.convert('liangzhu1','STD')
        else:
            print "Not a file!"
        print("Possible style:laser3 laser4 future3 water2 water3")
        style=input('Please input style you`d like to use')
        while True:
            print("Possible Quality:LOFI STD HIFI")
            quality=input('Please input the quality you`d like to use')
            if quality in ['STD','LOFI','HIFI']:
                break
        convert(style,quality)
        

    
