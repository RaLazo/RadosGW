import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from graphic import gui_branding


class RGWC(gui_branding):

    def __init__(self):
        super().__init__()
        self.init()
    
    def init(self):  
        self.table(3)  
        self.tabs()
        self.set_helpdesk()
        self.window()
        self.statusBar().showMessage('STATE: Programm running . . .')
        self.set_menubar()
        self.set_actions()
        self.set_toolbar()
        self.show()

app = QApplication(sys.argv)
w=RGWC()
sys.exit(app.exec_())