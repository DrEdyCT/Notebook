#!/usr/bin/python
# -*- coding: utf-8 -*-
# -*- coding: ascii -*-

import sys, form
from PyQt4 import QtGui, QtCore
import datetime
from data_base import PersonModel, cur
from form import Ui_Form


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

            item = QtGui.QTableWidgetItem(row[1])
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
        self.reminder()

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

            self.reminder()

    def delRow(self):
        selected = self.tableWidget.currentRow()
        if selected == -1:
            pass
        else:
            self.tableWidget.removeRow(selected)
            self.person.delRow(selected)
        self.reminder()

    def reminder(self):
        items = self.person.items_list
        if len(items) != 0:
            rows = items[-1][-1]
        else: rows = 0
        n = 0; size = 0
        text = ''
        while n != int(rows):
            my_date = items[n][3]
            now_date = datetime.date.today()
            delta = datetime.timedelta(days=1)
            if str(my_date) == str(now_date):
                text += u'%s сегодня справляет День Рождения\n' % items[n][1]
                size += 20
            elif str(now_date + delta) == str(my_date):
                text += u'%s завтра будет справлять День Рождения\n' % items[n][1]
                size += 20
            n += 1
        if size > 60: size = 60
        self.textEdit.setMaximumSize(QtCore.QSize(16777215, size))
        self.textEdit.setText(text)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    MyForm = Notebook()
    MyForm.show()
    sys.exit(app.exec_())