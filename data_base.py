#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3

db = sqlite3.connect('PersonModel.db')
cur = db.cursor()

class PersonModel(object):
    def createTable(self):
        cur.execute('CREATE TABLE IF NOT EXISTS notebook (id INTEGER PRIMARY KEY, name VARCHAR(255), phone_number VARCHAR(12), birthday VARCHAR, row_number VARCHAR(255))')
        db.commit()
        cur.execute('SELECT row_number FROM notebook')
        row_list = cur.fetchall()
        if len(row_list) != 0:
            self.row_number = int(row_list[-1][0]) + 1
        else: self.row_number = 1
        cur.execute('SELECT * FROM notebook')
        db.commit()

    def saveRow(self, row_id, name, phone_number = '', birthday = ''):
        self.row_id = row_id
        self.name = name
        self.phone_number = phone_number
        self.birthday = birthday
        cur.execute('INSERT INTO notebook (id, name, phone_number, birthday, row_number) VALUES (%i, %s, %s, %s, %i)'
                    % (self.row_id, self.name, self.phone_number, self.birthday, self.row_number))
        self.row_number += 1
        db.commit()

    def delRow(self, row_number):
        row_number += 1
        cur.execute('DELETE FROM notebook WHERE row_number = %i' % row_number)
        db.commit()

        new_row_number = row_number
        while row_number != self.row_number:
            cur.execute('UPDATE notebook SET row_number = %i WHERE row_number = %i' % (new_row_number, row_number + 1))
            row_number += 1
            new_row_number += 1

        self.row_number -= 1

    @property
    def table_id(self):
        cur.execute('SELECT id FROM notebook')
        id_list = cur.fetchall()
        if len(id_list) != 0:
             last_id = id_list[-1][0]
        else: last_id = 0
        return last_id + 1

