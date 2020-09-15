# 此文件存储数据库相关方法
import sqlite3
from classes import *
from basic import *


class DataBase:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.book_table = 'bookTable'
        self.booklist_table = 'booklistTable'
        self.author_table = 'authorTable'
        self.history_table = 'historyTable'
        self.book_table_created = False
        self.author_table_created = False
        self.history_table_created = False
        self.booklist_table_created = False

    def connect(self):
        self.conn = sqlite3.connect('info.db')
        self.cursor = self.conn.cursor()

    def close(self):
        self.conn.commit()
        self.conn.close()

    # 新建书籍表, 记住建表操作只能进行一次
    def createBookTable(self):
        if self.book_table_created:
            return
        self.connect()
        self.cursor.execute('create table %s (ID int primary key, name text, authors text, pub_date text,'
                            ' publisher text, isbn text, language text, cover_path text, rating int,'
                            ' file_path text, tags text, booklists text)' % self.book_table)
        self.book_table_created = True
        self.close()

    # 新建书单表
    def createBooklistTable(self):
        if self.booklist_table_created:
            return
        self.connect()
        self.cursor.execute('create table %s (name text primary key, books text)' % self.booklist_table)
        self.booklist_table_created = True
        self.close()

    # 新建历史搜索表
    def createHistoryTable(self):
        if self.history_table_created:
            return
        self.connect()
        self.cursor.execute('create table %s (time text primary key, content text)' % self.history_table)
        self.history_table_created = True
        self.close()

    # 新建作者表
    def createAuthorTable(self):
        if self.author_table_created:
            return
        self.connect()
        self.cursor.execute('create table %s (ID int primary key, name text, books text)' % self.author_table)
        self.author_table_created = True
        self.close()

    # 获取所有书籍，返回一个Book类型的列表
    # 每次打开应用，应该调用一下该函数，把所有书籍存储起来
    def getAllBooks(self):
        books = []
        self.connect()
        ret = self.cursor.execute('select * from %s' % self.book_table)
        for row in ret:
            book = Book(*row)
            books.append(book)
        self.close()
        return books

    # 对书籍进行模糊搜索, attr_name对应数据库表的相应属性名，value则是需要查询的值(不支持列表，只能单个查询)
    def getBooksFuzzy(self, attr_name, value):
        books = []
        self.connect()
        ret = self.cursor.execute('select * from %s where %s like "%%%s%%" ' % (self.book_table, attr_name, value))
        for row in ret:
            book = Book(*row)
            books.append(book)
        self.close()
        return books

    # 对书籍进行精确的搜索
    def getBooksAccurate(self, attr_name, value):
        books = []
        self.connect()
        ret = self.cursor.execute('select * from %s where %s=%s' % (self.book_table, attr_name, value))
        for row in ret:
            book = Book(*row)
            books.append(book)
        self.close()
        return books

    # 根据作者ID进行检索，返回书籍ID列表
    def getBooksByAuthor(self, author_id):
        self.connect()
        ret = self.cursor.execute('select * from %s where id=%d ' % (self.book_table, author_id))
        books = parseBooks(ret[0][2])
        self.close()
        return books

    # 根据书单名进行检索，返回书籍ID列表
    def getBooksByList(self, list_name):
        self.connect()
        ret = self.cursor.execute('select * from %s where name=%s' % list_name)
        books = parseBooks(ret[0][1])
        self.close()
        return books

    # 获取所有的历史记录，返回一个History列表
    def getAllHistory(self):
        histories = []
        self.connect()
        ret = self.cursor.execute('select * from %s' % self.history_table)
        for row in ret:
            history = History(*row)
            histories.append(history)
        self.close()
        return histories






