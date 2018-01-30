import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class popup(QWidget) :
    def __init__(self,windowtyp):
        QWidget.__init__(self) 
        self.setGeometry(300,300,240,320)
        self.setWindowTitle('Pop up') 
        self.setFixedSize(100,200)
        self.show()


