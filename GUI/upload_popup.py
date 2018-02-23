import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from rgwclass2 import rgw

class Create_Popup(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 200, 300, 300)
        self.resize(300,300)
        self.setWindowTitle("Create")
        self.setWindowIcon(QIcon("icon/create.svg"))
        layout = QFormLayout()
        l1 = QLabel() 
        l2 = QLabel()
        l1.setAlignment(Qt.AlignCenter)
        l1.setFont(QFont("Calibri", 11, QFont.Bold))
        l1.setText("Create Bucket")
        l2.setText("Name:")
        self.name = QLineEdit(self)
        self.button = QPushButton("Create", self)
        self.button.clicked.connect(self.on_click)
        layout.addRow(l1)
        layout.addRow(l2)
        layout.addRow(self.name)
        layout.addRow(self.button)
        self.setLayout(layout)
        self.show()        
    
    def on_click(self):
        file = open("../UserData.txt","r") 
        string=file.read()
        file.close()
        string=string.split("\n")    
        self.r=rgw(string[0],string[1],string[2])
        self.r.bucketname=str(self.name.text())
        self.r.create()
        self.close()
