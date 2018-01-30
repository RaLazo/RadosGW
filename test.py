import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from rgwclass2 import rgw

class RGWC(QMainWindow,QTabWidget):

    def __init__(self):
        super().__init__()
        self.init()
    
    def init(self):
        k=rgw('C8QE7PRORJGH4B52ZOZ7','VfuN9KgJaFfkL0POJbkVJ8FnpzaRgTHzowfj3Xy3','172.16.136.3')
        k.bn('test')
        b=k.lists()
        self.table = QTableWidget() 
        self.setCentralWidget(self.table)
        [self.table.insertRow(i) for i in range(len(b))]
        [self.table.insertColumn(i) for i in [0,1,2]]
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

        self.docked = QDockWidget("HelpDesk", self)
        self.addDockWidget(Qt.RightDockWidgetArea, self.docked)
        self.dockedWidget = QWidget(self)
        self.tabs = QTabWidget()
        self.tab1 = QWidget()	
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tabs.addTab(self.tab1,"RGWC")
        self.tabs.addTab(self.tab2,"Buckets")
        self.tabs.addTab(self.tab3,"Objects")
        
        label = QLabel(self)
        pixmap = QPixmap('RGWC.PNG')
        label.setPixmap(pixmap)
        self.docked.setWidget(self.tabs)
        #self.docked.setWidget(li[1])
        self.setWindowTitle("Rados Gateway Connector")
        self.setWindowIcon(QIcon("GUI/icon/cloud.svg"))
        self.setGeometry(100,100,700,500)
        #QToolTip.setFont(QFont('Arial', 14))
        #button = QPushButton("Drück mich",self)
        #button.setToolTip("This is a <b>button<b>") #kleines Beschreibungsfenster
        #button.move(100,100)
        #button.clicked.connect(self.ged)
        self.statusBar().showMessage('STATUS: Programm start')
        
        # Definition of the menubar
        menubar = self.menuBar()
        file = menubar.addMenu('&Start')
        option = menubar.addMenu('&Options')
        help = menubar.addMenu('&Help')
        
        # Definition of the actions
        exitMe = QAction(QIcon('GUI/icon/exit.svg'),'&Exit',self)
        delete = QAction(QIcon('GUI/icon/delete.svg'),'&Delete',self)
        upload = QAction(QIcon('GUI/icon/upload.svg'),'&Upload',self)
        download = QAction(QIcon('GUI/icon/download.svg'),'&Download',self)
        public = QAction(QIcon('GUI/icon/public.svg'),'&Public',self)
        private = QAction(QIcon('GUI/icon/private.svg'),'&Private',self)
        account = QAction(QIcon('GUI/icon/account.svg'),'&Account',self)
        create = QAction(QIcon('GUI/icon/create.svg'),'&Create',self)
        # Function of exit
        exitMe.setShortcut('Ctrl+E')
        exitMe.triggered.connect(self.close)
        file.addAction(exitMe)
        # function of help
        helplink = QAction('&more. . .',self)
        helplink.triggered.connect(self.openUrl)
        help.addAction(helplink)
        #Function of delete
        delete.setShortcut('CTRL+B')
        delete.triggered.connect(self.delete_bucket)
        #Definition of the toolbar
        toolbarbucket = self.addToolBar('Tools')
        toolbarbucket.addAction(account)
        toolbarbucket.addAction(create)
        toolbarbucket.addAction(delete)
        toolbarbucket.addAction(upload)
        toolbarbucket.addAction(download)
        toolbarbucket.addAction(private)
        toolbarbucket.addAction(public)
        
        #show the window
        self.show()

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

    def delete_bucket(self):
        choice = QMessageBox.question(self,'Delte a Bucket','Are you sure ?',QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            sys.exit()
        else:
            pass

app = QApplication(sys.argv)
w=RGWC()
sys.exit(app.exec_())


