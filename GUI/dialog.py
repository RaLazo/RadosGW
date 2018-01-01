# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setEnabled(True)
        Dialog.resize(618, 325)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon/ceph-icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        Dialog.setSizeGripEnabled(False)
        self.treeView = QtWidgets.QTreeView(Dialog)
        self.treeView.setGeometry(QtCore.QRect(0, 10, 371, 261))
        self.treeView.setObjectName("treeView")
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(380, 10, 231, 261))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.comboBox = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.comboBox.setObjectName("comboBox")
        self.verticalLayout.addWidget(self.comboBox)
        self.lineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)
        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout.addWidget(self.pushButton_3)
        self.progressBar = QtWidgets.QProgressBar(Dialog)
        self.progressBar.setGeometry(QtCore.QRect(10, 290, 591, 24))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.treeView.raise_()
        self.verticalLayoutWidget.raise_()
        self.pushButton_3.raise_()
        self.progressBar.raise_()
        self.progressBar.raise_()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "RadosGW_Connector"))
        self.pushButton.setText(_translate("Dialog", "Create"))
        self.pushButton_2.setText(_translate("Dialog", "Delete"))
        self.pushButton_3.setText(_translate("Dialog", "Upload"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

