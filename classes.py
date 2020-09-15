# 此文件存储核心的类
from database import *


class Book:
    def __init__(self, ID=0, name="", authors=None, pub_date="", publisher="", cover_path="", isbn="", language="", file_path="", tags=None):
        if tags is None:
            tags = []
        if authors is None:
            authors = []
        self.ID = ID
        self.name = name
        self.authors = authors
        self.pub_date = pub_date
        self.publisher = publisher
        self.isbn = isbn
        self.lanuage = language
        self.cover_path = cover_path  # 封面的存储位置，通过此信息加载封面
        self.rating = None
        self.file_path = file_path  # 文件位置，可以根据此信息打开文件
        self.tags = tags  # 书籍的标签
        self.bookLists = []  # 所属的书单

    # 修改基础信息
    def setName(self, new_name):
        self.name = new_name
        # 需要修改数据库中的数据

    def setAuthors(self, new_authors):
        self.authors = new_authors
        # 需要修改数据库中的数据

    def setPub_date(self, new_date):
        self.pub_date = new_date
        # 需要修改数据库中的数据

    def setIsbn(self, new_isbn):
        self.isbn = new_isbn
        # 需要修改数据库中的数据

    def setPublisher(self, new_publisher):
        self.publisher = new_publisher
        # 需要修改数据库中的数据

    def setLanguage(self, new_language):
        self.lanuage = new_language
        # 需要修改数据库中的数据

    def setCover(self, new_cover):
        self.cover_path = new_cover
        # 需要修改数据库中的数据

    def setRating(self, new_rating):
        self.rating = new_rating
        # 需要修改数据库中的数据

    def setFile_path(self, new_path):
        self.file_path = new_path
        # 需要修改数据库中的数据

    # 修改数据库内书籍的信息
    def updateDB(self):

        pass

    # 打开当前书籍
    def openBook(self):
        pass

    # 关闭当前书籍
    def closeBook(self):
        pass

    # 把当前书添加到某个书单中
    def addToList(self, list_name):
        pass

    # 自动生成封面，可选功能
    def generateCover(self):
        pass

    # 生成二维码，分享给别人
    def QRcode(self):
        pass


class Author:
    def __init__(self, books=None):
        if books is None:
            books = []
        self.books = books

    def addBook(self, book):
        pass

    def deleteBook(self, book):
        pass

    # 更新数据库的信息
    def updateDB(self):
        pass


class BookList:
    def __init__(self, books=None):
        if books is None:
            books = []
        self.books = books

    def share(self):
        pass

    def addBook(self, book):
        self.books.append(book)

    def deleteBook(self, book):
        self.books.remove(book)

    # 更新数据库信息
    def updateDB(self):
        pass

