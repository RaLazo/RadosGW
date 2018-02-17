import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QAction
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import *
from PyQt5.uic import *

app = QApplication(sys.argv)

def mixCocktail(_str):
      print(_str)


widget = loadUi('drinkmixer.ui')

widget.btn_ckt1.clicked.connect(lambda: micCocktail("string"))

widget.show()
sys.exit(app.exec_())