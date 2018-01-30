from PyQt5 import QtWidgets, QtGui, QtCore


class Main(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        # create table:
        self.table = QtWidgets.QTableWidget()
        [self.table.insertRow(i) for i in [0,1,2]]
        [self.table.insertColumn(i) for i in [0,1]]
        # set values for first column:
        self.table.setItem(0, 1, QtWidgets.QTableWidgetItem('A') )
        self.table.setItem(1, 1, QtWidgets.QTableWidgetItem('B') )
        self.table.setItem(2, 1, QtWidgets.QTableWidgetItem('C') )
        # add checkboxes to second column:
        a = []
        for i in range(3):
            a.append(QtWidgets.QCheckBox( parent=self.table ))
            self.table.setCellWidget(i, 0, a[i])
            a[i].clicked.connect(self.checkbox_clicked)
    
        # connect table signals:
        self.table.cellChanged.connect(self.cell_changed)
        self.table.itemChanged.connect(self.item_changed)
        # connect checkbox signals:
        # show:
        self.setCentralWidget(self.table)
        self.setWindowTitle('TableWidget, CheckBoxes')
        self.show()

    def cell_changed(self, row, col):
        print(row, col)
    def checkbox_clicked(self, checked):
        print(checked)
    def item_changed(self, item):
        print(item)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main = Main()
    app.exec_()