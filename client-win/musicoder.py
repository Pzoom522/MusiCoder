from gui import Window
from PyQt4 import QtGui
import sys

app = QtGui.QApplication(sys.argv)

#initialize the main window
window = Window(app)
Window.w = window

#make sure wait message is set before connecting procedure starts
app.processEvents()

#because initializing client will take some time
window.initClient(True)

sys.exit(app.exec_())
