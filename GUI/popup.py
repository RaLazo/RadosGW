# Title: RadosGW - GUI - Popup
# Eng.: Rafael Lazenhofer
# Ver.: 1.0
# Date: 02.03.2018
#
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
        self.resize(300,300)
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
        file = open("../UserData.txt","w") 
        file.write(str(self.secertkey.text())+"\n"+str(self.accountkey.text())+"\n"+str(self.host.text()))
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

