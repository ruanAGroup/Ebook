# 此文件存储数据库相关方法
import sqlite3
from basic import listToString, parseRetBooks, parseRetAuthors, parseRetBooklists, parseListString
from classes import Author, BookList, Book, History


class DataBase:
    db_name = 'test.db'
    book_table = 'bookTable'
    booklist_table = 'booklistTable'
    author_table = 'authorTable'
    history_table = 'historyTable'

    # 新建书籍表, 记住建表操作只能进行一次
    @staticmethod
    def createBookTable():
        conn = sqlite3.connect(DataBase.db_name)
        cursor = conn.cursor()
        cursor.execute('create table %s (ID int primary key, name text, authors text, pub_date text,'
                       ' publisher text, isbn text, language text, cover_path text, rating int,'
                       ' file_path text, tags text, booklists text))' % DataBase.book_table)
        conn.commit()
        conn.close()

    # 新建书单表
    @staticmethod
    def createBooklistTable():
        conn = sqlite3.connect(DataBase.db_name)
        cursor = conn.cursor()
        cursor.execute('create table %s (name text primary key, books text)' % DataBase.booklist_table)
        conn.commit()
        conn.close()

    # 新建历史搜索表
    @staticmethod
    def createHistoryTable():
        conn = sqlite3.connect(DataBase.db_name)
        cursor = conn.cursor()
        cursor.execute('create table %s (time text primary key, content text)' % DataBase.history_table)
        conn.commit()
        conn.close()

    # 新建作者表
    @staticmethod
    def createAuthorTable():
        conn = sqlite3.connect(DataBase.db_name)
        cursor = conn.cursor()
        cursor.execute('create table %s (name text primary key , books text)' % DataBase.author_table)
        conn.commit()
        conn.close()

    # 获取所有书籍，返回一个Book类型的列表
    @staticmethod
    def getAllBooks():
        conn = sqlite3.connect(DataBase.db_name)
        cursor = conn.cursor()
        ret = cursor.execute('select * from %s' % DataBase.book_table)
        conn.commit()
        conn.close()
        books = parseRetBooks(ret)
        if not books:
            return None
        return books

    # 传入一个书籍ID，获取该书籍的INFO属性
    @staticmethod
    def getBookINFOByID(ID):
        conn = sqlite3.connect(DataBase.db_name)
        cursor = conn.cursor()
        ret = cursor.execute('select * from %s where ID=%s' % (DataBase.book_table, ID))
        conn.commit()
        conn.close()
        books = parseRetBooks(ret)
        if not books:
            return None
        return books[0].INFO

    # 对书籍进行模糊搜索, attr_name对应数据库表的相应属性名，value则是需要查询的值(不支持列表，只能单个查询)
    @staticmethod
    def getBooksFuzzy(attr_name, value):
        conn = sqlite3.connect(DataBase.db_name)
        cursor = conn.cursor()
        ret = cursor.execute('select * from %s where %s like "%%%s%%" ' % (DataBase.book_table, attr_name, value))
        conn.commit()
        conn.close()
        books = parseRetBooks(ret)
        if not books:
            return None
        return books

    # 对书籍进行精确的搜索
    @staticmethod
    def getBooksAccurate(attr_name, value):
        conn = sqlite3.connect(DataBase.db_name)
        cursor = conn.cursor()
        ret = cursor.execute("select * from %s where %s='%s'" % (DataBase.book_table, attr_name, value))
        conn.commit()
        conn.close()
        books = parseRetBooks(ret)
        if not books:
            return None
        return books

    # 获取所有书单
    @staticmethod
    def getAllBookLists():
        conn = sqlite3.connect(DataBase.db_name)
        cursor = conn.cursor()
        ret = cursor.execute('select * from %s' % DataBase.booklist_table)
        conn.commit()
        conn.close()
        booklists = parseRetBooklists(ret)
        if not BookList:
            return None
        return booklists

    # 根据书单名进行检索，返回书籍ID列表
    @staticmethod
    def getBooksByList(list_name):
        books = []
        conn = sqlite3.connect(DataBase.db_name)
        cursor = conn.cursor()
        ret = cursor.execute("select * from %s where name='%s'" % (DataBase.booklist_table, list_name))
        for row in ret:
            ID = parseListString(row[2])
            books.append(ID)
        conn.commit()
        conn.close()
        return books

    # 获取所有的历史记录，返回一个History列表
    @staticmethod
    def getAllHistory():
        conn = sqlite3.connect(DataBase.db_name)
        cursor = conn.cursor()
        ret = cursor.execute('select * from %s' % DataBase.history_table)
        histories = []
        for row in ret:
            time = row[0]
            content = row[1]
            history = History(time, content)
            histories.append(history)
        conn.commit()
        conn.close()
        return histories

    # 获取所有作者
    @staticmethod
    def getAllAuthors():
        conn = sqlite3.connect(DataBase.db_name)
        cursor = conn.cursor()
        ret = cursor.execute('select * from %s' % DataBase.author_table)
        conn.commit()
        conn.close()
        authors = parseRetAuthors(ret)
        if not authors:
            return None
        return authors

    # 根据作者名进行检索，返回书籍ID列表
    @staticmethod
    def getBooksByAuthor(author_name):
        conn = sqlite3.connect(DataBase.db_name)
        cursor = conn.cursor()
        ret = cursor.execute("select * from %s where name='%s'" % (DataBase.author_table, author_name))
        books = []
        for row in ret:
            ID = parseListString(row[2])
            books.append(ID)
        conn.commit()
        conn.close()
        if not books:
            return None
        return books

    # 传入一个作者的name，获取相应的Author对象
    @staticmethod
    def getAuthorByName(name):
        conn = sqlite3.connect(DataBase.db_name)
        cursor = conn.cursor()
        ret = cursor.execute("select * from %s where name='%s'" % (DataBase.author_table, name))
        conn.commit()
        conn.close()
        authors = parseRetAuthors(ret)
        if not authors:
            return None
        return authors[0]

    # 传入一个Book对象，添加到数据库中
    @staticmethod
    def addBook(book):
        conn = sqlite3.connect(DataBase.db_name)
        cursor = conn.cursor()
        cursor.execute("insert into %s values(%s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s' ,'%s')" % (
            DataBase.book_table, book.ID, book.name, listToString(book.authors), book.pub_date, book.publisher,
            book.isbn, book.language, book.cover_path, book.rating, book.file_path, listToString(book.tags),
            listToString(book.bookLists)))
        conn.commit()
        conn.close()

    # 传入一个Book对象，从数据库中删除
    @staticmethod
    def deleteBook(book):
        conn = sqlite3.connect(DataBase.db_name)
        cursor = conn.cursor()
        cursor.execute('delete from %s where id=%s' % (DataBase.book_table, book.ID))
        conn.commit()
        conn.close()

    # 传入一个Book对象，更新数据库中的数据
    @staticmethod
    def updateBook(book):
        conn = sqlite3.connect(DataBase.db_name)
        cursor = conn.cursor()
        cursor.execute("update %s set name='%s', authors='%s', pub_date='%s', publisher='%s', isbn='%s', "
                       "language='%s', cover_path='%s', rating='%s', file_path='%s', tags='%s', booklists='%s' where "
                       "ID=%s" % (
                           DataBase.book_table, book.name, listToString(book.authors), book.pub_date, book.publisher,
                           book.isbn, book.language, book.cover_path, book.rating, book.file_path,
                           listToString(book.tags),
                           listToString(book.bookLists), book.ID))
        conn.commit()
        conn.close()

    # 传入一个Book对象，倘若书籍在数据库中，则返回True,否则返回False
    @staticmethod
    def bookInDB(book):
        if not DataBase.getBookINFOByID(book.ID):
            return False
        return True

    # 传入一个Author对象，倘若作者在数据库中，返回True，否则False
    @staticmethod
    def authorInDB(author):
        if not DataBase.getAuthorByName(author.name):
            return False
        return True

    @staticmethod
    def addAuthor(author):
        conn = sqlite3.connect(DataBase.db_name)
        cursor = conn.cursor()
        cursor.execute("insert into %s values('%s', '%s')" % (DataBase.author_table, author.name,
                                                              listToString(author.books)))
        conn.commit()
        conn.close()

    @staticmethod
    def deleteAuthor(author):
        conn = sqlite3.connect(DataBase.db_name)
        cursor = conn.cursor()
        cursor.execute("delete from %s where name='%s'" % (DataBase.author_table, author.name))
        conn.commit()
        conn.close()

    @staticmethod
    def updateAuthor(author):
        conn = sqlite3.connect(DataBase.db_name)
        cursor = conn.cursor()
        cursor.execute("update %s set books='%s' where name='%s'" % (DataBase.author_table, listToString(author.books),
                                                                     author.name))
        conn.commit()
        conn.close()

    @staticmethod
    def addHistory(history):
        conn = sqlite3.connect(DataBase.db_name)
        cursor = conn.cursor()
        cursor.execute("insert into %s values('%s', '%s')" % (DataBase.history_table, history.time, history.content))
        conn.commit()
        conn.close()

    @staticmethod
    def deleteHistory(history):
        conn = sqlite3.connect(DataBase.db_name)
        cursor = conn.cursor()
        cursor.execute("delete from %s where time='%s'" % (DataBase.history_table, history.time))
        conn.commit()
        conn.close()

    @staticmethod
    def booklistInDB(booklist):
        if not DataBase.getBooksByList(booklist.name):
            return False
        return True

    @staticmethod
    def addBooklist(booklist):
        conn = sqlite3.connect(DataBase.db_name)
        cursor = conn.cursor()
        cursor.execute("insert into %s values('%s', '%s')" % (DataBase.booklist_table, booklist.name,
                                                              listToString(booklist.books)))
        conn.commit()
        conn.close()

    @staticmethod
    def deleteBooklist(booklist):
        conn = sqlite3.connect(DataBase.db_name)
        cursor = conn.cursor()
        cursor.execute("delete from %s where name='%s'" % (DataBase.booklist_table, booklist.name))
        conn.commit()
        conn.close()

    @staticmethod
    def updateBooklist(booklist):
        conn = sqlite3.connect(DataBase.db_name)
        cursor = conn.cursor()
        cursor.execute("update %s set books='%s' where name='%s'" % (DataBase.booklist_table,
                                                                     listToString(booklist.books), booklist.name))
        conn.commit()
        conn.close()
