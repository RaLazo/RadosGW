'''
  RadosGW - GUI - Popup adaption to the RadosGW - Connector
    Copyright (C) 2017  Rafael Lazenhofer

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
# Ist für das Accountpopup zuständig
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from rgwclass2 import rgw

class Account_Popup(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 200, 300, 300)
        #self.resize(300,300)
        self.setWindowTitle("Account")
        self.setWindowIcon(QIcon("icon/account.svg"))
        layout = QFormLayout()
        l1 = QLabel() 
        l2 = QLabel()
        l3 = QLabel()
        l4 = QLabel()
        l1.setAlignment(Qt.AlignCenter)
        l1.setFont(QFont("Calibri", 11, QFont.Bold))
        l1.setText("Account Data")
        l2.setText("Accountkey:")
        l3.setText("Secretkey:")
        l4.setText("Host:")
        self.secertkey = QLineEdit(self)
        self.accountkey = QLineEdit(self)
        self.host = QLineEdit(self)
        self.button = QPushButton("Update", self)
        self.button.clicked.connect(self.on_click)
        layout.addRow(l1)
        layout.addRow(l2)
        layout.addRow(self.secertkey)
        layout.addRow(l3)
        layout.addRow(self.accountkey)
        layout.addRow(l4)
        layout.addRow(self.host)
        layout.addRow(self.button)
       
        self.setLayout(layout)
        self.show()
        
    
    def on_click(self):
        file = open("UserData.txt","w") 
        file.write(str(self.secertkey.text())+"\n"+str(self.accountkey.text())+"\n"+str(self.host.text()))
        file.close()
        self.close()

class Admin_Popup(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 200, 300, 300)
        self.resize(300,300)
        self.setWindowTitle("Admin")
        self.setWindowIcon(QIcon("icon/account.svg"))
        layout = QFormLayout()
        l1 = QLabel() 
        l2 = QLabel()
        l3 = QLabel()
        l4 = QLabel()
        l1.setAlignment(Qt.AlignCenter)
        l1.setFont(QFont("Calibri", 11, QFont.Bold))
        l1.setText("Account Data")
        l2.setText("Host:")
        l3.setText("User:")
        l4.setText("Password:")
        self.secertkey = QLineEdit(self)
        self.accountkey = QLineEdit(self)
        self.host = QLineEdit(self)
        self.button = QPushButton("Update", self)
        self.button.clicked.connect(self.on_click)
        layout.addRow(l1)
        layout.addRow(l2)
        layout.addRow(self.secertkey)
        layout.addRow(l3)
        layout.addRow(self.accountkey)
        layout.addRow(l4)
        layout.addRow(self.host)
        layout.addRow(self.button)
       
        self.setLayout(layout)
        self.show()
        
    
    def on_click(self):
        file = open("../UserData.txt","w") 
        file.write(str(self.secertkey.text())+"\n"+str(self.accountkey.text())+"\n"+str(self.host.text()))
        self.close()

