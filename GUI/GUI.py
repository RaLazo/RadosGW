import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from rgwclass2 import rgw


class RGWC(QMainWindow,QTabWidget):
    def init(self):  
       
        
        self.docked = QDockWidget("HelpDesk", self)
        self.addDockWidget(Qt.RightDockWidgetArea, self.docked)
        self.dockedWidget = QWidget(self)
        self.docked.setWidget(self.dockedWidget)
        self.dockedWidget.setLayout(QVBoxLayout())
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


