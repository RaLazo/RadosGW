'''
  RadosGW - Connector - Class adaption to the RadosGW - GUI - Executeable
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
import sys
import json
import paramiko
from io import StringIO
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from popup import Account_Popup
from rgwclass2 import rgw
import ctypes
myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)


class gui_branding(QMainWindow,QTabWidget):
    
    def __init__(self):
        '''
        Intialisieren der GUI Klasse
        '''
        super().__init__()
        file = open("UserData.txt","r") 
        string=file.read()
        file.close()
        string=string.split("\n")
        try:
            self.r=rgw(string[0],string[1],string[2])
            self.r.dp=string[3]
            self.host=string[2]
        except IndexError:
            self.account_data()
        self.check = []
        self.checkb = []
        self.checkx = []

    def tabs(self):
        '''
        Initialisiert die Tabs die sich
        im Helpdesk befinden
        '''
        self.tabs = QTabWidget()
        self.tab1 = QWidget()	
        self.tab2 = QWidget()
        self.tabs.addTab(self.tab1,"RGWC")
        self.tabs.addTab(self.tab2,"Tools")
        self.tab_1()
        self.tab_2()
        self.admin_conector()
    
    def tab_3(self):
        '''
        Initialisiert das Admin Tab
        '''
        layout = QFormLayout()
        l1 = QLabel() 
        text=QLabel()
        text.setText("Create a user")
        button_layout=QHBoxLayout()
        self.createbox = QLineEdit()
        self.createbox.editingFinished.connect(self.create_user)
        check_button=QPushButton("Mark all",self)
        check_button.clicked.connect(self.set_check)
        button = QPushButton("Show all users",self)
        button.clicked.connect(self.show_all_users)
        #data_button = QPushButton("Show User Data",self)
        #data_button.clicked.connect(self.show)
        l1.setAlignment(Qt.AlignCenter)
        l1.setFont(QFont("Calibri", 11, QFont.Bold))
        button_layout.addWidget(check_button)
        button_layout.addWidget(button)
        layout.addRow(text)
        layout.addRow(self.createbox)
        layout.addRow(button_layout)
        #layout.addRow(data_button)
        self.tab3.setLayout(layout)
    
    def admin_conector(self):
        '''
        Diese Methode baut eine SSH Verbindung zu
        einem Speichercluster um die Funktionen des Admin Tabs
        nutzen zu können.
        '''
        try:
            file=open('AdminData.txt','r')
            string = file.read()
            try:
                string=string.split("\n") 
                ip=string[0]
                port=string[1]
                username=string[2]
                password=string[3]
                self.tab3 = QWidget()
                self.tabs.addTab(self.tab3,"Admin")
                self.tab_3()
                self.ssh=paramiko.SSHClient()
                self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self.ssh.connect(ip,port,username,password)
            except IndexError:
                pass
        except FileNotFoundError:
            pass   
        
    
    def show_all_users(self):
        '''
        Zeigt alle User eines Speichercluster an
        '''
        self.statusBar().showMessage('STATUS: looking for users . . .')   
        a=[]
        cmd='radosgw-admin metadata list user' 
        stdin,stdout,stderr=self.ssh.exec_command(cmd)
        outlines=stdout.readlines()
        resp=''.join(outlines)
        resp=resp.split("\"")
        for i in range(len(resp)):
            
            if resp[i].find("[") == -1:
                if resp[i].find(",") == -1:
                     if resp[i].find("]") == -1:
                        a.append(resp[i])
        self.statusBar().showMessage('STATUS: Completed')   
        self.set_table2(a)

    def create_user(self):
        '''
        erstellt einenn User 
        '''
        self.statusBar().showMessage('STATUS: creating User . . .')   
        cmd = "radosgw-admin user create --uid="+self.createbox.text()+" --display-name="+self.createbox.text()+" >> s3_user_data/"+self.createbox.text()+".txt"
        self.ssh.exec_command(cmd)
        self.statusBar().showMessage('STATUS: Completed')   

    def delete_users(self):
        self.statusBar().showMessage('STATUS: deleting . . .')
        for i in range(len(self.check)):
            self.statusBar().showMessage('STATUS: '+str(i)+' of '+str(len(self.check)))
            cmd ="radosgw-admin user rm --uid="+self.check[i]
            self.ssh.exec_command(cmd)
        self.statusBar().showMessage('STATUS: Updating table . . .')    
        self.show_all_users()
        self.statusBar().showMessage('STATUS: Completed')  
        

    def tab_1(self):
        '''
        Initialisiert das Tab in der Willkommenstext steht
        und der Downloadpath gesetzt wird 
        '''
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
        self.tab1.setLayout(layout)
    
    def downpath(self):
        '''
        Für das setzen des Downloadpaths
        '''
        self.r.dp = str(QFileDialog.getExistingDirectory(self, "Select Directory"))

    def set_bucket_groupbox(self):
        '''
        dated die "Your buckets" up die sich im
        zweiten Tab "Tools" des "HelpDesk" befindet
        '''
        try:
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
        except AttributeError:
            pass
        
    def tab_2(self):
        '''
        Initialisiert die das zweite Tab "Tools" des
        "HelpDesks" 
        '''
        layout = QFormLayout()
        button_layout=QHBoxLayout()
        setext=QLabel()
        cetext=QLabel()
        bucket_button=QPushButton("Mark all",self)
        bucket_button_show=QPushButton("Show the Buckets",self)
        self.searchbox = QLineEdit()
        self.cb = QLineEdit()
        setext.setText("Search for an Object")
        cetext.setText("Create a Bucket")
        button_layout.addWidget(bucket_button)
        button_layout.addWidget(bucket_button_show)
        bucket_button_show.clicked.connect(lambda: self.set_table(self.r.lists()))
        bucket_button_show.clicked.connect(self.set_bucket_groupbox)
        bucket_button.clicked.connect(self.set_check)
        self.cb.editingFinished.connect(self.createbucket)
        self.searchbox.editingFinished.connect(self.textchange)
        layout.addRow(setext)
        layout.addRow(self.searchbox)
        layout.addRow(cetext)
        layout.addRow(self.cb)
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.set_bucket_groupbox()
        layout.addWidget(self.scroll)
        layout.addRow(button_layout)
        self.tab2.setLayout(layout)

    def createbucket(self):
        '''
        Erzeugt einen Bucket wenn die bestimmten Parameter
        passen (z.B.: mehr als 3 Zeichen)
        '''
        self.statusBar().showMessage('STATUS: Creating a bucket . . .')
        if ((self.r.bn(self.cb.text()) == 0) and (self.cb.text()!="") and (len(self.cb.text())>3)):
            self.r.bucketname=self.cb.text()
            self.r.create()
            self.set_table(self.r.lists())
            self.set_bucket_groupbox()
            self.cb.setText("")
            self.statusBar().showMessage('STATUS: Completed')
        else:
             self.statusBar().showMessage('STATUS: ERROR this bucket can´t be created')

    def textchange(self): 
        '''
        Sucht nach den Objekten die im Suchfeld vom zweiten Tab "Tools"
        eingegeben werden.
        '''
        if self.r.bucketname != "empty":
            help_array = []
            help = self.list_objects() 
            for i in range(len(help)):  
                if str(self.searchbox.text()) in help[i]: 
                    help_array.append(help[i]) 
            self.set_table(help_array) 
    
    def radio(self, rb):
        '''
        Überprüft die Radiobuttons in der "Your buckets" Box vom
        zweiten Tab "Tools" und setz den Bucketnamen und dated die
        Tabelle up mit den Objekten des Buckets up
        '''
        del self.checkb [:] 
        for i in range(len(rb)):
            if str(rb[i].isChecked()) == "True":
               self.r.bn(rb[i].text())
               self.set_table(self.list_objects())
               
    def set_check(self): 
        '''
        Setzt alle Elemente der Table auf True also hakt sie ab
        (wird in von dem Button "Mark All" im zweiten Tab des "HelpDesks" verwendet)
        '''
        for i in range (len(self.checkb)): 
            if self.checkb[i].isChecked() == True: 
                self.checkb[i].setChecked(False) 
            else: 
                self.checkb[i].setChecked(True) 
        self.checker(self.checkb, self.checkx) 
        
    def window(self):
        '''
        setzt die Fensterparameter des RGWC
        '''
        self.setWindowTitle("Rados Gateway Connector")
        self.setWindowIcon(QIcon("icon/RGWC.PNG"))
        self.setGeometry(500,250,800,500)

    def set_menubar(self):
        '''
        Initialisiert die Menuebar des RGWC - GUI
        '''
        self.menubar = self.menuBar()
        self.file = self.menubar.addMenu('&Start')
        self.option = self.menubar.addMenu('&Options')
        self.help = self.menubar.addMenu('&Help')
    
    def set_optinon(self):
        '''
        Initialisert die den Button für den "HelpDesk"
        '''
        self.helpdesk.setShortcut('CTRL+H')
        self.helpdesk.triggered.connect(self.set_helpdesk)
        self.option.addAction(self.helpdesk)

    def set_exit_function(self):
        '''
        Initialisert die den Button für das Beenden des Programs
        '''
        self.exitMe.setShortcut('Ctrl+Q')
        self.exitMe.triggered.connect(self.closeit)
        self.file.addAction(self.exitMe)

    def set_help_function(self):
        '''
        Initialisert die Hilfe 
        '''
        self.helplink = QAction('&more. . .',self)
        self.helplink.triggered.connect(self.openUrl)
        self.help.addAction(self.helplink)

    def delete_something(self):
        '''
        Initialisert den "Delete" Button
        '''
        self.delete.setShortcut('CTRL+R')
        self.delete.triggered.connect(self.delete_window)
        self.option.addAction(self.delete)
    
    def closeit(self):
        '''
        schließt das Programm
        '''
        self.close()
        try:
            self.ssh.close()
        except (AttributeError):
            pass
        try:
            self.popup_a.close()
        except (AttributeError):
            pass
        

    def set_account(self):
        '''
        Initialisert den "Account" Button
        '''
        self.account.setShortcut('CTRL+A')
        self.account.triggered.connect(self.account_data)
        self.file.addAction(self.account)
    
    def set_upload(self):
        '''
        Initialisert den "Uploader" Button
        '''
        self.upload.setShortcut('CTRL+U')
        self.upload.triggered.connect(self.openFileNamesDialog)
        self.option.addAction(self.upload)
    
    def set_download(self):
        '''
        Initialisert den "Download" Button
        '''
        self.download.setShortcut('CTRL+D')
        self.download.triggered.connect(self.download_something)
        self.option.addAction(self.download)

    def set_rights(self):
        '''
        Initialisert die Buttons für die Rechte
        '''
        self.public.setShortcut("CTRL+P")
        self.private.setShortcut("CTRL+V")
        self.public.triggered.connect(lambda: self.right(0))
        self.private.triggered.connect(lambda: self.right(1))
        self.option.addAction(self.public)
        self.option.addAction(self.private)
    
    def right(self, right):
        '''
        Mit dieser Methode werden die Rechte geändert
        '''
        self.statusBar().showMessage('STATUS: Chaning Permissions . . . ')
        if right == 1: 
            for i in range(len(self.check)):
                self.r.rights_mangement(self.check[i],1)
        else:
             for i in range(len(self.check)):
                self.r.rights_mangement(self.check[i],0)
        self.set_table(self.list_objects())     
        self.statusBar().showMessage('STATUS: Completed')       


    def download_something(self):
        '''
        Mit dieser Methode werden Daten in den dafür vorgesehenen
        Ordner gedownloadet
        '''
        self.statusBar().showMessage('STATUS: Downloading . . .')
        if self.check:
            check_len=len(self.check)
            for i in range(check_len):
                self.r.downloader(self.check[i])
                self.statusBar().showMessage('STATUS: Downloading Data '+str(i)+' of '+str(check_len))
            self.set_table(self.list_objects())
            self.statusBar().showMessage('STATUS: Completed ')
        else:
             self.statusBar().showMessage('STATUS: ERROR can´t download this object')

    def account_data(self):
        self.popup_a=Account_Popup()

    def set_helpdesk(self):
        '''
        setzt den "HelpDesk" bzw. initialiesirt in
        '''
        try:
            del self.docked
        except AttributeError:
            pass
        self.docked = QDockWidget("HelpDesk", self)
        self.addDockWidget(Qt.RightDockWidgetArea, self.docked)
        self.docked.setWidget(self.tabs)    

    def openFileNamesDialog(self):  
        '''
        Diese Methode ist für den Upload von Daten zuständig
        '''
        self.statusBar().showMessage('STATUS: opening the upload section') 
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self,"Upload your Data", "","All Files (*);;Python Files (*.py)", options=options)
        if files:
            self.statusBar().showMessage('STATUS: Uploading . . .') 
            upload_num=len(files)
            for i in range(upload_num):
                self.r.uploader(files[i])
                self.statusBar().showMessage('STATUS: Uploading Data '+str(i)+' of '+str(upload_num)) 
            self.set_table(self.list_objects())

            self.statusBar().showMessage('STATUS: Completed')
        else:
             self.statusBar().showMessage('STATUS: ERROR during the upload')

    
    def set_actions(self):
        '''
        Initialsiert die einzelenen Actions der Tool & Menuebar
        '''
        self.exitMe = QAction(QIcon('icon/exit.svg'),'&Exit',self)
        self.delete = QAction(QIcon('icon/delete.svg'),'&Delete',self)
        self.upload = QAction(QIcon('icon/upload.svg'),'&Upload',self)
        self.download = QAction(QIcon('icon/download.svg'),'&Download',self)
        self.public = QAction(QIcon('icon/public.svg'),'&Public',self)
        self.private = QAction(QIcon('icon/private.svg'),'&Private',self)
        self.account = QAction(QIcon('icon/account.svg'),'&Account',self)
        self.helpdesk = QAction(QIcon("icon/option.svg"),'&Helpdesk',self)
        self.set_exit_function()
        self.set_help_function()
        self.set_optinon()
        self.set_account()
        self.set_upload()
        self.set_download()
        self.set_rights()

    def set_toolbar(self):
        '''
        Initialiesiert die Toolbar
        '''
        self.toolbarbucket = self.addToolBar('Tools')
        self.toolbarbucket.addAction(self.account)
        self.toolbarbucket.addAction(self.exitMe)
        self.toolbarbucket.addAction(self.delete)
        self.toolbarbucket.addAction(self.upload)
        self.toolbarbucket.addAction(self.download)
        self.toolbarbucket.addAction(self.private)
        self.toolbarbucket.addAction(self.public)
        self.delete_something()

    def openUrl(self):
        '''
        Ist für die "Help" der Menuebar zuständig
        und öffnet unter dem Punkt "more . . ." den Link
        zum Github Repository des RGWC
        '''
        url = QUrl('https://github.com/RaLazo/RadosGW/wiki/RGWC---GUI')
        if not QDesktopServices.openUrl(url):
            QMessageBox.warning(self, 'Open Url', 'Could not open url')

    def delete_window(self):
        '''
        Diese Methode ist für das Löschen von Buckets & Objects verantwortlich
        '''
        choice = QMessageBox.question(self,'garbage can','Are you sure ?',QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            if self.table_output_type == 0:
                if self.r.bucketname != "empty":
                    self.statusBar().showMessage('STATUS: Starting delete process . . .') 
                    a = self.list_objects()
                    for i in range(len(a)):
                        b=a[i].split()
                        for j in range(len(self.check)):
                            if b[0] == self.check[j]:
                                 self.r.delete_object(self.check[j])
                    self.set_table(self.list_objects())

                a = self.r.lists()
                for i in range(len(a)):
                    b=a[i].split()
                    for j in range(len(self.check)):
                        if b[0] == self.check[j]:
                            self.r.bucketname = self.check[j]
                            self.r.delete()
                            self.set_table(self.r.lists())
                            self.set_bucket_groupbox()
                            self.r.bucketname = "empty"
                self.statusBar().showMessage('STATUS: Completed')
            else:
                self.delete_users()
        else:
            pass
        
    def table(self,colums):
        '''
        Initialisiert die Tabele für das Programm
        '''
        self.table = QTableWidget() 
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        self.setCentralWidget(self.table)
        [self.table.insertColumn(i) for i in range(colums)]
        width = self.table.verticalHeader().width()
        width += self.table.horizontalHeader().length()+100
    '''
    def set_table2(self,b):
        del self.table
        a=[]
        self.table(2)
        [self.table.insertRow(i) for i in range(len(b))]
        x=[]
        for i in range(len(b)):
            x.append(b[i].split()[0])
            a.append(QCheckBox(str(i),parent=self.table))
            self.table.setCellWidget(i, 0, a[i])
            a[i].clicked.connect(lambda: self.checker(a,x))
            self.table.setItem(i, 1, QTableWidgetItem(x[i]))
        self.checkx = x 
        self.checkb = a 
        self.table_output_type=1
    '''        
    def set_table2(self,b):
        del self.table
        a=[]
        self.table(2)
        [self.table.insertRow(i) for i in range(len(b))]
        x=[]
        for i in range(len(b)):
            y=b[i].split()[0]
            x.append(QPushButton(y,self))
            a.append(QCheckBox(str(i),parent=self.table))
            self.table.setCellWidget(i, 0, a[i])
            self.table.setCellWidget(i, 1, x[i])
            a[i].clicked.connect(lambda: self.checker(a,x))
            x[i].clicked.connect(lambda: self.get_user_info(y))
            #self.table.setItem(i, 1, QTableWidgetItem(x[i]))
        self.checkx = x 
        self.checkb = a 
        self.table_output_type=1
    
    def get_user_info(self,y):
        self.statusBar().showMessage('STATUS: Collecting userdata . . .') 
        cmd='radosgw-admin user info --uid='+y 
        stdin,stdout,stderr=self.ssh.exec_command(cmd)
        outlines=stdout.readlines()
        output = ""
        for line in outlines:
            output = output + line.strip()
        io= StringIO(output)
        data = json.load(io)
        for element in data['keys']:
            output = "User: "+element['user'] + '\n'
            output = output+"Acceskey: "+ element['access_key'] +'\n'
            output = output+"Secretkey: "+ element['secret_key']
        cb = QApplication.clipboard()
        cb.clear(mode=cb.Clipboard)
        cb.setText(output, mode=cb.Clipboard)
        QMessageBox.about(self, "Userdata", output)
        self.statusBar().showMessage('STATUS: Completed')
    def set_table(self,b):
        '''
        Fügt bzw. formiert die Tabelle je nach gebrauch um bzw. fügt 
        Daten hinzu & löscht auch diese
        '''
        del self.table
        self.table(5)
        object=1
        try:
            b[0].split()[2]
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
        self.checkx = x 
        self.checkb = a 
        self.table_output_type=0

    def checker(self,a,x):
        '''
        Überprüft welche Elemente der 
        Table angehakt sind und speichert diese 
        in ein Array
        '''
        del self.check[:]
        for i in range(len(a)):
            if str(a[i].isChecked())=="True":
                self.check.append(x[i])

    def list_objects(self):
        '''
        Lists the objects of an bucket
        RETURN VALUE:
            [object_name] [object_size] [modification_date]
        '''
        b=[]
        bucket = self.r.conn.get_bucket(self.r.bucketname)
        i=0
        for key in bucket.list():
            i=self.updating(i)
            if(len(str(key.get_acl()))== 42):
                rigth = "Privat"
            else:
                rigth="Public"
            b.append("{name} {size} {modified} {acl}".format(
                    name = key.name,
                    size = key.size,
                    modified = key.last_modified,
                    acl = rigth,
                    ))
        self.statusBar().showMessage('STATUS: Completed') 
        return b        
    
    def updating(self, i):
        string='Updating '
        if i<4:
            for j in range(i):
                string = string+'. '
            self.statusBar().showMessage(string) 
            i=i+1
        else:
            self.statusBar().showMessage(string)
            string='Updating ' 
            i=0
        return i