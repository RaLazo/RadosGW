import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from popup import Account_Popup
from popup import Create_Popup
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
        self.checkb = []
        self.checkx = []
    
    def set_helpdesk(self):
        self.docked = QDockWidget("HelpDesk", self)
        self.addDockWidget(Qt.RightDockWidgetArea, self.docked)
        self.dockedWidget = QWidget(self)
        self.docked.setWidget(self.tabs)

    def tabs(self):
        self.tabs = QTabWidget()
        self.tab1 = QWidget()	
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tabs.addTab(self.tab1,"RGWC")
        self.tabs.addTab(self.tab2,"Tools")
        self.tab_1()
        self.tab_2()
    
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
        setext=QLabel()
        setext.setText("Search for an Object")
        bucket_button=QPushButton("Mark all",self)
        bucket_button_show=QPushButton("Show the Buckets",self)
        button_layout.addWidget(bucket_button)
        button_layout.addWidget(bucket_button_show)
        bucket_button_show.clicked.connect(lambda: self.set_table(self.r.lists()))
        bucket_button_show.clicked.connect(self.set_bucket_groupbox)
        bucket_button.clicked.connect(self.set_check)
        self.searchbox = QLineEdit()
        self.searchbox.textChanged.connect(self.textchange)
        layout.addRow(setext)
        layout.addRow(self.searchbox)
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.set_bucket_groupbox()
        layout.addWidget(self.scroll)
        layout.addRow(button_layout)
        self.tab2.setLayout(layout)
    
    def textchange(self):
        help_array = []
        help = self.r.list_objects()
        for i in range(len(help)): 
            if str(self.searchbox.text()) in help[i]:
                help_array.append(help[i])
        self.set_table(help_array)


    def radio(self, rb):
        for i in range(len(rb)):
            if str(rb[i].isChecked()) == "True":
               self.r.bn(rb[i].text())
               self.set_table(self.r.list_objects())

        
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
        self.file.addAction(self.create)
    
    def set_upload(self):
        self.upload.setShortcut('CTRL+U')
        self.upload.triggered.connect(self.openFileNamesDialog)
        self.file.addAction(self.upload)
    
    def set_download(self):
        self.download.setShortcut('CTRL+D')
        self.download.triggered.connect(self.download_something)
        self.file.addAction(self.download)

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
        self.statusBar().showMessage('STATUS: Starting Upload . . . ')
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self,"Upload your Data", "","All Files (*);;Python Files (*.py)", options=options)
        if files:
            for i in range(len(files)):
                self.r.uploader(files[i])
            self.set_table(self.r.list_objects())
        self.statusBar().showMessage('STATUS: Completed ')

    
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
        self.statusBar().showMessage('STATUS: Start remove of  . . . ')
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
        self.statusBar().showMessage('STATUS: Completed ')
    def helpdesk_back(self):
        del self.docked
        self.set_helpdesk()
        
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
        del self.checkb [:]
        self.table(5)
        object=1
        try:
            b[1].split()[2]
        except IndexError:
            object=0
            del self.table
            self.table(3)

        [self.table.insertRow(i) for i in range(len(b))]
        a = []
        x = []
        q = []
        for i in range(len(b)):
            x.append(b[i].split()[0])
            y=b[i].split()[1]
            a.append(QCheckBox(str(i),parent=self.table))
            self.table.setCellWidget(i, 0, a[i])
            a[i].clicked.connect(lambda: self.checker(a,x))
            self.table.setItem(i, 1, QTableWidgetItem(x[i]))
            self.table.setItem(i, 2, QTableWidgetItem(y))
            if object == 1:
               q=b[i].split()[3]
               z=b[i].split()[2]
               self.table.setItem(i,3,QTableWidgetItem(z))
               self.table.setItem(i,4,QTableWidgetItem(q))
        self.checkx = x
        self.checkb = a

    def checker(self,a,x):
        del self.check[:]
        for i in range(len(a)):
            if a[i].isChecked()== True:
                self.check.append(x[i])

    def set_check(self):
        for i in range (len(self.checkb)):
            if self.checkb[i].isChecked() == True:
                self.checkb[i].setChecked(False)
            else:
                self.checkb[i].setChecked(True)
        self.checker(self.checkb, self.checkx)


           
