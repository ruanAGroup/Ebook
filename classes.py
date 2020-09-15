# 此文件存储核心的类
from database import *


class Book:
    def __init__(self, ID=0, name="", authors=None, pub_date="", publisher="", isbn="", language="", cover_path="",
                 rating=0, file_path="", tags=None, bookLists=None):
        if bookLists is None:
            bookLists = []
        if tags is None:
            tags = []
        if authors is None:
            authors = []
        self.ID = ID  # 序号，每本书的序号将作为它的关键码，不能有重复，对用户是不可见的
        self.name = name
        self.authors = authors
        self.pub_date = pub_date
        self.publisher = publisher
        self.isbn = isbn  # 以字符串形式存储
        self.lanuage = language
        self.cover_path = cover_path  # 封面的存储位置，通过此信息加载封面
        self.rating = rating  # 评分，int型数据，1星到5星，0表示未评分
        self.file_path = file_path  # 文件位置，可以根据此信息打开文件
        self.tags = tags  # 书籍的标签，列表
        self.bookLists = bookLists  # 所属的书单，列表
        self.isOpen = False  # 书籍是否已经打开

    # 修改基础信息
    def setName(self, new_name):
        self.name = new_name
        self.updateDB()  # 修改数据库中的数据

    def setAuthors(self, new_authors):
        self.authors = new_authors
        self.updateDB()  # 修改数据库中的数据

    def setPub_date(self, new_date):
        self.pub_date = new_date
        self.updateDB()  # 修改数据库中的数据

    def setIsbn(self, new_isbn):
        self.isbn = new_isbn
        self.updateDB()  # 修改数据库中的数据

    def setPublisher(self, new_publisher):
        self.publisher = new_publisher
        self.updateDB()  # 修改数据库中的数据

    def setLanguage(self, new_language):
        self.lanuage = new_language
        self.updateDB()  # 修改数据库中的数据

    def setCover(self, new_cover):
        self.cover_path = new_cover
        self.updateDB()  # 修改数据库中的数据

    def setRating(self, new_rating):
        self.rating = new_rating
        self.updateDB()  # 修改数据库中的数据

    def setFile_path(self, new_path):
        self.file_path = new_path
        self.updateDB()  # 修改数据库中的数据

    def setTags(self, new_tags):
        self.tags = new_tags
        self.updateDB()

    # 把当前书添加到某个书单中
    # 调用此函数时要确保不传入没有意义的名字，比如说空字符串和只有空格的字符串
    def addToList(self, list_name):
        self.bookLists.append(list_name)
        self.updateDB()

    # 修改数据库内书籍的信息
    def updateDB(self):

        pass

    # 打开当前书籍
    def openBook(self):
        self.isOpen = True
        # 与UI界面的按钮对接，打开阅读器窗口

    # 关闭当前书籍
    def closeBook(self):
        # 与UI界面按钮对接，关闭书籍是记得调用此函数以改变isOpen的状态
        self.isOpen = False

    # 自动生成封面，可选功能
    def generateCover(self):
        pass

    # 生成二维码，分享给别人，可选功能
    def QRcode(self):
        pass


class Author:
    def __init__(self, ID, name, books=None):
        if books is None:
            books = []
        self.ID = ID  # 因为作者可能同名，所以要有一个关键码ID
        self.name = name
        self.books = books  # 书籍的ID列表

    def addBook(self, book):
        self.books.append(book)
        pass

    def deleteBook(self, book):
        if book in self.books:
            self.books.remove(book)
            if not self.books:
                # 已经没有该作者写的书了，应该在数据库中删去该作者的信息
                pass
            else:
                self.updateDB()
        else:
            # 出错
            pass

    # 更新数据库的信息
    def updateDB(self):
        pass


class BookList:
    def __init__(self, name, books=None):
        if books is None:
            books = []
        self.name = name
        self.books = books  # 书籍的ID列表

    def addBook(self, book):
        self.books.append(book)
        self.updateDB()

    def deleteBook(self, book):
        self.books.remove(book)
        # 书单内书的数量为空时，不需要删去该书单
        self.updateDB()

    # 更新数据库信息
    def updateDB(self):
        pass

    # 可选功能，书单分享，生成一张分享图片
    def share(self):
        pass


class History:
    def __init__(self, time="", content=""):
        self.time = time
        self.content = content

    # 添加到数据库中
    def addToDB(self):
        pass

