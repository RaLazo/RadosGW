import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
#from rgwclass2 import rgw
import ctypes
myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

class gui_branding(QMainWindow,QTabWidget):
    
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
        label = QLabel()
        pixmap = QPixmap('icon/RGWC_small.PNG')
        label.setPixmap(pixmap)
        label.setAlignment(Qt.AlignCenter)
        l1 = QLabel()
        l2 = QLabel()
        l3 = QLabel()
        l4 = QLabel()    
        l1.setAlignment(Qt.AlignCenter)
        l2.setAlignment(Qt.AlignCenter)
        l3.setAlignment(Qt.AlignCenter)
        l1.setText("Welcome to")
        l2.setText("Rados Gateway Connector")
        l3.setText("Desktop - Client")
        l1.setFont(QFont("Calibri", 15, QFont.Bold))
        l2.setFont(QFont("Calibri", 10, QFont.Bold))
        l3.setFont(QFont("Calibri", 10, QFont.Bold))
        layout.addRow(label)
        layout.addRow(l1)
        layout.addRow(l2)
        layout.addRow(l3)
        # Optional, resize window to image size
        self.resize(pixmap.width(),pixmap.height())
        self.tab1.setLayout(layout)

    def tab_2(self):
        layout = QFormLayout()
        layout.addRow("Searching",QLineEdit())
        [layout.addWidget(QRadioButton("bucket"+str(i),self.tab2)) for i in range(10)]
        self.tab2.setLayout(layout)
    
    def tab_3(self):
        layout = QFormLayout()
        layout.addRow("Searching",QLineEdit())
        self.tab3.setLayout(layout)
        
    def window(self):
        self.setWindowTitle("Rados Gateway Connector")
        self.setWindowIcon(QIcon("icon/RGWC.PNG"))
        self.setFixedSize(700,500)

    def set_menubar(self):
        self.menubar = self.menuBar()
        self.file = self.menubar.addMenu('&Start')
        self.option = self.menubar.addMenu('&Options')
        self.help = self.menubar.addMenu('&Help')
    
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

    def set_actions(self):
        self.exitMe = QAction(QIcon('icon/exit.svg'),'&Exit',self)
        self.delete = QAction(QIcon('icon/delete.svg'),'&Delete',self)
        self.upload = QAction(QIcon('icon/upload.svg'),'&Upload',self)
        self.download = QAction(QIcon('icon/download.svg'),'&Download',self)
        self.public = QAction(QIcon('icon/public.svg'),'&Public',self)
        self.private = QAction(QIcon('icon/private.svg'),'&Private',self)
        self.account = QAction(QIcon('icon/account.svg'),'&Account',self)
        self.create = QAction(QIcon('icon/create.svg'),'&Create',self)
        self.set_exit_function()
        self.set_help_function()

    def set_toolbar(self):
        self.toolbarbucket = self.addToolBar('Tools')
        self.toolbarbucket.addAction(self.account)
        self.toolbarbucket.addAction(self.exitMe)
        self.toolbarbucket.addAction(self.delete)
        self.toolbarbucket.addAction(self.create)
        self.toolbarbucket.addAction(self.upload)
        self.toolbarbucket.addAction(self.download)
        self.toolbarbucket.addAction(self.private)
        self.toolbarbucket.addAction(self.public)
        self.delete_something()

    def checkbox_clicked(self, checked):
        print(checked)

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
        choice = QMessageBox.question(self,'Delte a Bucket','Are you sure ?',QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            sys.exit()
        else:
            pass

    def table(self):
        b=['object date','object date','object date','object date','object date','object date','object date','object date','object date','object date']
        self.table = QTableWidget() 
        self.setCentralWidget(self.table)
        [self.table.insertRow(i) for i in range(len(b))]
        [self.table.insertColumn(i) for i in [0,1,2]]
        width = self.table.verticalHeader().width()
        width += self.table.horizontalHeader().length()
        if self.table.verticalScrollBar().isVisible():
            width += self.table.verticalScrollBar().width()
        width += self.table.frameWidth() * 30
        self.table.setFixedWidth(width)
        a=[]
        y=[]
        for i in range(len(b)):
            del y[:]
            y=b[i].split()
            a.append(QCheckBox( parent=self.table ))
            self.table.setCellWidget(i, 0, a[i])
            a[i].clicked.connect(self.checkbox_clicked)
            self.table.setItem(i, 1, QTableWidgetItem(y[0]))
            self.table.setItem(i, 2, QTableWidgetItem(y[1]))