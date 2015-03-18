#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, form
from PyQt4 import QtGui, QtCore
from data_base import PersonModel, cur


class Notebook(QtGui.QWidget, form.Ui_Form):
    person = PersonModel()
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)
        self.connect(self.pushButton, QtCore.SIGNAL('clicked()'), self.saveRow)
        self.connect(self.calendarWidget, QtCore.SIGNAL('selectionChanged()'), self.inputDate)
        self.connect(self.pushButton_2, QtCore.SIGNAL('clicked()'), self.delRow)

        self.person.createTable()
        
        rows = 0
        for row in cur:
            self.tableWidget.setRowCount(rows + 1)

            item = QtGui.QTableWidgetItem(str(row[1]))
            item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsEnabled)
            self.tableWidget.setItem(rows, 0, item)
            item = QtGui.QTableWidgetItem(row[2])
            item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsEnabled)
            self.tableWidget.setItem(rows, 1, item)
            item = QtGui.QTableWidgetItem(row[3])
            item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsEnabled)
            self.tableWidget.setItem(rows, 2, item)

            rows += 1

        self.tableWidget.resizeColumnsToContents()
        self.rows = rows

    def inputDate(self):
        date = self.calendarWidget.selectedDate()
        self.lineEdit_3.setText(str(date.toPyDate()))

    def saveRow(self):
        row_id = self.person.table_id

        name = self.lineEdit.text()
        phone_number = self.lineEdit_2.text()
        birthday = self.lineEdit_3.text()

        if name != '':

            self.tableWidget.setRowCount(self.person.row_number)

            item = QtGui.QTableWidgetItem(name)
            item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsEnabled)
            name = "'%s'" % name
            self.tableWidget.setItem(self.person.row_number-1, 0, item)

            item = QtGui.QTableWidgetItem(phone_number)
            item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsEnabled)
            phone_number = "'%s'" % phone_number
            self.tableWidget.setItem(self.person.row_number-1, 1, item)

            item = QtGui.QTableWidgetItem(birthday)
            item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsEnabled)
            birthday = "'%s'" % birthday
            self.tableWidget.setItem(self.person.row_number-1, 2, item)

            self.person.saveRow(row_id, name, phone_number, birthday)
            self.tableWidget.resizeColumnsToContents()
            self.rows += 1

    def delRow(self):
        selected = self.tableWidget.currentRow()
        if selected == -1:
            pass
        else:
            self.tableWidget.removeRow(selected)
            self.person.delRow(selected)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    MyForm = Notebook()
    MyForm.show()
    sys.exit(app.exec_())