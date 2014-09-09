#!/usr/bin/python
#-*- coding: utf-8 -*-
import sqlite3 as lite
import sys

name = 'cover'
file_name = '/home/ruben/Рабочий стол/Проект-Увечье/cover.jpg'


class DBConnect():
    """Class to work with database"""
    def __init__(self, db_name):
        self.con = lite.connect(db_name)
        self.con.text_factory = str
        self.cursor = self.con.cursor()
        self.cursor.execute(
            'CREATE TABLE IF NOT EXISTS artworks(name VARCHAR(50) PRIMARY KEY, data BLOB)'
        )

    def add_image(self, name, data):
        '''
        This method adds image to the database. 
        Requires argument name as a pk and image data.
        ''' 
        with self.con:
            data = lite.Binary(data)
            self.cursor.execute('INSERT OR REPLACE INTO artworks(name, data) VALUES (?,?)', (name, data))

    def get_image(self, name):
        '''
        This method gets image from the database.
        Requires argument name as a pk.
        '''  
        with self.con:
            self.cursor.execute('SELECT data FROM artworks WHERE name=?', (name,))
            data = self.cursor.fetchone()
            return str(data[0])


    
if __name__ == '__main__':
    inst = DBConnect('GPlayer.db')            
    def readImage(file_name):
        try:
            file =  open(file_name, 'rb')
            return file.read()
        except IOError:
            print('IOError!')  
            sys.exit()  
        finally:
            file.close()    

    img = readImage(file_name)         
    #inst.add_image(name+'3', img)
    #file = open('result.jpg', 'wb')
    #file.write(inst.get_image(name))
    inst.get_image(name)