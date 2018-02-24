import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from account_popup import Account_Popup
from create_popup import Create_Popup
from rgwclass2 import rgw
import ctypes
myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)



class gui_branding(QMainWindow,QTabWidget):
    
    def __init__(self):
        super().__init__()
        file = open("../UserData.txt","r") 
        string=file.read()
        file.close()
        string=string.split("\n")    
        self.r=rgw(string[0],string[1],string[2])
        self.r.dp=string[3]
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
        self.r.dp = str(QFileDialog.getExistingDirectory(self, "Select Directory"))

    def set_bucket_groupbox(self):
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
        self.scroll.setWidget(mygroupbox)

        
    def tab_2(self):
        layout = QFormLayout()
        button_layout=QHBoxLayout()
        bucket_button=QPushButton("Search",self)
        bucket_button_show=QPushButton("Show all",self)
        button_layout.addWidget(bucket_button)
        button_layout.addWidget(bucket_button_show)
        bucket_button_show.clicked.connect(lambda: self.set_table(self.r.lists()))
        bucket_button_show.clicked.connect(self.set_bucket_groupbox)
        layout.addRow("Searching",QLineEdit())
        layout.addRow(button_layout)
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.set_bucket_groupbox()
        layout.addWidget(self.scroll)
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
        self.exitMe.triggered.connect(self.closeit)
        self.file.addAction(self.exitMe)

    def set_help_function(self):
        self.helplink = QAction('&more. . .',self)
        self.helplink.triggered.connect(self.openUrl)
        self.help.addAction(self.helplink)

    def delete_something(self):
        self.delete.setShortcut('CTRL+R')
        self.delete.triggered.connect(self.delete_window)
        self.option.addAction(self.delete)
    
    def closeit(self):
        self.close()
        try:
            self.popup_a.close()
        except AttributeError:
            pass
        try:
            self.popup_c.close()
        except AttributeError:
            pass
        

    def set_account(self):
        self.account.setShortcut('CTRL+A')
        self.account.triggered.connect(self.account_data)
        self.file.addAction(self.account)
    
    def set_create(self):
        self.create.setShortcut('CTRL+C')
        self.create.triggered.connect(self.create_something)
        self.option.addAction(self.create)
    
    def set_upload(self):
        self.upload.setShortcut('CTRL+U')
        self.upload.triggered.connect(self.openFileNamesDialog)
        self.option.addAction(self.upload)
    
    def set_download(self):
        self.download.setShortcut('CTRL+D')
        self.download.triggered.connect(self.download_something)
        self.option.addAction(self.download)

    def set_rights(self):
        self.public.setShortcut("CTRL+P")
        self.private.setShortcut("CTRL+V")
        self.public.triggered.connect(lambda: self.right(0))
        self.private.triggered.connect(lambda: self.right(1))
        self.option.addAction(self.public)
        self.option.addAction(self.private)
    
    def right(self, right):
        
        self.statusBar().showMessage('STATUS: Chaning Permissions . . . ')
        if right == 1: 
            for i in range(len(self.check)):
                self.r.rights_mangement(self.check[i],1)
        else:
             for i in range(len(self.check)):
                self.r.rights_mangement(self.check[i],0)
        self.set_table(self.r.list_objects())     
        self.statusBar().showMessage('STATUS: Completed')       


    def download_something(self):
        self.statusBar().showMessage('STATUS: Downloading . . .')
        for i in range(len(self.check)):
            self.r.downloader(self.check[i])
        self.set_table(self.r.list_objects())
        self.statusBar().showMessage('STATUS: Completed ')

    def create_something(self):
        self.popup_c = Create_Popup()
    
    def account_data(self):
        self.popup_a=Account_Popup()
        

    def openFileNamesDialog(self):   
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self,"Upload your Data", "","All Files (*);;Python Files (*.py)", options=options)
        if files:
            for i in range(len(files)):
                self.r.uploader(files[i])
            self.set_table(self.r.list_objects())

    
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
        self.set_create()
        self.set_upload()
        self.set_download()
        self.set_rights()

    def set_toolbar(self):
        self.toolbarbucket = self.addToolBar('Tools')
        self.toolbarbucket.addAction(self.account)
        self.toolbarbucket.addAction(self.exitMe)
        self.toolbarbucket.addAction(self.create)
        self.toolbarbucket.addAction(self.delete)
        self.toolbarbucket.addAction(self.upload)
        self.toolbarbucket.addAction(self.download)
        self.toolbarbucket.addAction(self.private)
        self.toolbarbucket.addAction(self.public)
        self.delete_something()

    def checkbox_clicked(self, box):
        print(box.text())

    def openUrl(self):
        url = QUrl('https://github.com/RaLazo/RadosGW')
        if not QDesktopServices.openUrl(url):
            QMessageBox.warning(self, 'Open Url', 'Could not open url')

    def delete_window(self):
        choice = QMessageBox.question(self,'garbage can','Are you sure ?',QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            if self.r.bucketname != "empty":
                a = self.r.list_objects()
                for i in range(len(a)):
                    b=a[i].split()
                    for j in range(len(self.check)):
                        if b[0] == self.check[j]:
                             self.r.delete_object(self.check[j])
                self.set_table(self.r.list_objects())
                self.set_bucket_groupbox()
            a = self.r.lists()
            for i in range(len(a)):
                b=a[i].split()
                for j in range(len(self.check)):
                    if b[0] == self.check[j]:
                        self.r.bucketname = self.check[j]
                        self.r.delete()
                        self.set_table(self.r.lists())
            self.r.bucketname = "empty"
        else:
            pass
    def helpdesk_back(self):
        self.docked.setWidget(self.tabs)
        
    def table(self,colums):
        self.table = QTableWidget() 
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        self.setCentralWidget(self.table)
        [self.table.insertColumn(i) for i in range(colums)]
        width = self.table.verticalHeader().width()
        width += self.table.horizontalHeader().length()+100
    
    def set_table(self,b):
        del self.table
        self.table(5)
        object=1
        try:
            b[1].split()[2]
        except IndexError:
            object=0
            del self.table
            self.table(3)
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
            if object == 1:
               z=b[i].split()[2]
               q=b[i].split()[3]
               self.table.setItem(i,3,QTableWidgetItem(z))
               self.table.setItem(i,4,QTableWidgetItem(q))

    def checker(self,a,x):
        del self.check[:]
        for i in range(len(a)):
            if str(a[i].isChecked())=="True":
                self.check.append(x[i])


           
