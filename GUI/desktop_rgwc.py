'''
  RadosGW - GUI - Executeable a programm to connect to a Ceph storagecluster
    Copyright (C) 2018  Rafael Lazenhofer

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
'''
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



 # Create and display the splash screen
app = QApplication(sys.argv)
splash_pix = QPixmap('icon/RGWC.PNG')
splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
splash.setMask(splash_pix.mask())
splash.show()
app.processEvents()
w=RGWC()
splash.finish(w)
sys.exit(app.exec_())