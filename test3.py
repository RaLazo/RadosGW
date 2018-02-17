import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Main(QMainWindow) :
    def __init__(self) :
        QMainWindow.__init__(self) 
        self.setGeometry(300,300,240,320) 
        self.show() 
        menubar  = self. menuBar() 
        filemenu = menubar. addMenu('&File') 
        new = QAction(QIcon('GUI/icon/cloud.svg'), 'New', self) 
        new.triggered.connect(self.pop) 
        filemenu.addAction(new) 

    def pop(self) :
        self.window = Pop()

class Pop(QWidget) :
    def __init__(self):
        QWidget.__init__(self) 
        self.setGeometry(300,300,240,320)
        self.setWindowTitle('Pop up') 
        self.show()

app = QApplication(sys.argv)
w=Main()
sys.exit(app.exec_())
