import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
#from popup import Pop
from rgwclass2 import rgw
import ctypes
myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)



class gui_branding(QMainWindow,QTabWidget):
    
    def __init__(self):
        super().__init__()
        file = open("../UserData.txt","r") 
        string=file.read()
        string=string.split("\n")    
        self.r=rgw(string[0],string[1],string[2])
        self.check = []

    def helpdesk(self):
        self.docked = QDockWidget("HelpDesk", self)
        self.addDockWidget(Qt.RightDockWidgetArea, self.docked)
        self.dockedWidget = QWidget(self)

    def tabs(self):
        self.tabs = QTabWidget()
        self.tab1 = QWidget()	
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tabs.addTab(self.tab1,"RGWC")
        self.tabs.addTab(self.tab2,"Buckets")
        self.tabs.addTab(self.tab3,"Objects")
        self.tab_1()
        self.tab_2()
        self.tab_3()
    
    def tab_1(self):
        layout = QFormLayout()
        l1 = QLabel() 
        label = QLabel(self)
        pixmap = QPixmap('icon/small_RGWC.PNG')
        label.setPixmap(pixmap)
        label.setAlignment(Qt.AlignCenter)
        l1.setAlignment(Qt.AlignCenter)
        l1.setText("Welcome to\nRados Gateway Connector\nDesktop - Client")
        l1.setFont(QFont("Calibri", 11, QFont.Bold))
        downbutton=QPushButton("set Downloadpath",self)
        downbutton.clicked.connect(self.downpath)
        layout.addRow(label)
        layout.addRow(l1)
        layout.addRow(downbutton)
        # Optional, resize window to image size
        self.tab1.setLayout(layout)
    
    def downpath(self):
        dialog = QFileDialog()
        self.folder_path = dialog.getExistingDirectory(None, "Select Folder")
        
    def tab_2(self):
        layout = QFormLayout()
        button_layout=QHBoxLayout()
        bucket_button=QPushButton("Search",self)
        bucket_button_show=QPushButton("Show all",self)
        button_layout.addWidget(bucket_button)
        button_layout.addWidget(bucket_button_show)
        bucket_button_show.clicked.connect(lambda: self.set_table(self.r.lists()))
        layout.addRow("Searching",QLineEdit())
        layout.addRow(button_layout)
        mygroupbox = QGroupBox('Your Buckets')
        myform = QFormLayout()
        k = []
        b=self.r.lists()
        for i in range(len(b)):
            k.append(b[i].split()[0])
        i=0
        Radiobutton = []
        for i in range(len(k)):
            Radiobutton.append(QRadioButton(k[i]))
            Radiobutton[i].clicked.connect(lambda:self.radio(Radiobutton))
            myform.addRow(Radiobutton[i])
        mygroupbox.setLayout(myform)
        scroll = QScrollArea()
        scroll.setWidget(mygroupbox)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)
        self.tab2.setLayout(layout)
    
    def radio(self, rb):
        for i in range(len(rb)):
            if str(rb[i].isChecked()) == "True":
               self.r.bn(rb[i].text())
               self.set_table(self.r.list_objects())

    def tab_3(self):
        layout = QFormLayout()
        layout.addRow("Searching",QLineEdit())
        button_layout=QHBoxLayout()
        button_layout=QHBoxLayout()
        bucket_button=QPushButton("Search",self)
        bucket_button_mark=QPushButton("Mark all",self)
        button_layout.addWidget(bucket_button)
        button_layout.addWidget(bucket_button_mark)
        layout.addRow(button_layout)
        self.tab3.setLayout(layout)
        
    def window(self):
        self.setWindowTitle("Rados Gateway Connector")
        self.setWindowIcon(QIcon("icon/RGWC.PNG"))
        self.setGeometry(100,100,800,500)

    def set_menubar(self):
        self.menubar = self.menuBar()
        self.file = self.menubar.addMenu('&Start')
        self.option = self.menubar.addMenu('&Options')
        self.help = self.menubar.addMenu('&Help')
    
    def set_optinon(self):
        self.helpdesk.setShortcut('CTRL+H')
        self.helpdesk.triggered.connect(self.helpdesk_back)
        self.option.addAction(self.helpdesk)

    def set_exit_function(self):
        self.exitMe.setShortcut('Ctrl+E')
        self.exitMe.triggered.connect(self.close)
        self.file.addAction(self.exitMe)

    def set_help_function(self):
        self.helplink = QAction('&more. . .',self)
        self.helplink.triggered.connect(self.openUrl)
        self.help.addAction(self.helplink)

    def delete_something(self):
        self.delete.setShortcut('CTRL+B')
        self.delete.triggered.connect(self.delete_window)
    
    def set_account(self):
        self.account.setShortcut('CTRL+A')
        self.account.triggered.connect(self.account_data)
        self.file.addAction(self.account)
    
    def account_data(self):
        self.popup=Account_Popup()

    def set_actions(self):
        self.exitMe = QAction(QIcon('icon/exit.svg'),'&Exit',self)
        self.delete = QAction(QIcon('icon/delete.svg'),'&Delete',self)
        self.upload = QAction(QIcon('icon/upload.svg'),'&Upload',self)
        self.download = QAction(QIcon('icon/download.svg'),'&Download',self)
        self.public = QAction(QIcon('icon/public.svg'),'&Public',self)
        self.private = QAction(QIcon('icon/private.svg'),'&Private',self)
        self.account = QAction(QIcon('icon/account.svg'),'&Account',self)
        self.create = QAction(QIcon('icon/create.svg'),'&Create',self)
        self.helpdesk = QAction(QIcon("icon/option.svg"),'&Helpdesk',self)
        self.set_exit_function()
        self.set_help_function()
        self.set_optinon()
        self.set_account()

    def set_toolbar(self):
        self.toolbarbucket = self.addToolBar('Tools')
        self.toolbarbucket.addAction(self.account)
        self.toolbarbucket.addAction(self.exitMe)
        self.toolbarbucket.addAction(self.delete)
        self.toolbarbucket.addAction(self.create)
        self.toolbarbucket.addAction(self.upload)
        self.toolbarbucket.addAction(self.download)
        #self.toolbarbucket.addAction(self.private)
        #self.toolbarbucket.addAction(self.public)
        self.delete_something()

    def checkbox_clicked(self, box):
        print(box.text())

    def ged(self):
        self.sender().move(200,200)# Sender ist theoretisch der Button
        return
    

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key()== Qt.Key_A:       # Tastatur Eingabe
            print("Hallo")                  # Gibt hier Hallo aus wenn A
                                            # Gedrückt wird
    def openUrl(self):
        url = QUrl('https://github.com/RaLazo/RadosGW')
        if not QDesktopServices.openUrl(url):
            QMessageBox.warning(self, 'Open Url', 'Could not open url')

    def delete_window(self):
        print(self.check)
        choice = QMessageBox.question(self,'garbage can','Are you sure ?',QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            sys.exit()
        else:
            pass
    def helpdesk_back(self):
        self.docked.setWidget(self.tabs)
        
    def table(self):
        self.table = QTableWidget() 
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        self.setCentralWidget(self.table)
        [self.table.insertColumn(i) for i in [0,1,2]]
        width = self.table.verticalHeader().width()
        width += self.table.horizontalHeader().length()+100
    
    def set_table(self,b):
        del self.table
        self.table()
        a=[]
        [self.table.insertRow(i) for i in range(len(b))]
        
        x = []
        for i in range(len(b)):
            x.append(b[i].split()[0])
            y=b[i].split()[1]
            a.append(QCheckBox(str(i),parent=self.table))
            self.table.setCellWidget(i, 0, a[i])
            a[i].clicked.connect(lambda: self.checker(a,x))
            self.table.setItem(i, 1, QTableWidgetItem(x[i]))
            self.table.setItem(i, 2, QTableWidgetItem(y))

    def checker(self,a,x):
        del self.check[:]
        for i in range(len(a)):
            if str(a[i].isChecked())=="True":
                self.check.append(x[i])

class Account_Popup(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 200, 100, 100)
        self.setWindowTitle("Account")
        self.setWindowIcon(QIcon("icon/account.svg"))
        layout = QFormLayout()
        l1 = QLabel() 
        label = QLabel(self)
        pixmap = QPixmap('icon/small_RGWC.PNG')
        label.setPixmap(pixmap)
        label.setAlignment(Qt.AlignCenter)
        l1.setAlignment(Qt.AlignCenter)
        l1.setText("Welcome to\nRados Gateway Connector\nDesktop - Client")
        l1.setFont(QFont("Calibri", 11, QFont.Bold))
        self.setLayout(layout)
        self.show()
       

    