# 此文件存储基础方法
from classes import Author, BookList, History, Book
from database import DataBase
from settings import GlobalVar


# 解析用户输入的tag字符串，
# 输入支持语法 `tag1, tag2, tag3, tag4`，应该允许用户输入多余的空格，但是显示的时候不显示多余的空格
# 此函数将将输入字符串转换成列表[tag1, tag2, tag3, tag4]并返回
def parseTags(input_str):
    temp_list = input_str.split(',')
    tag_list = []
    for i in temp_list:
        tag_list.append(i.strip())
    return tag_list


# 此函数将解析后的tag列表再转换成一个字符串
def tagsToString(tag_list):
    if not tag_list:
        return ""
    tag_str = ""
    for tag in tag_list:
        tag_str += tag
        tag_str += ", "
    tag_str -= ", "
    return tag_str


def parseListString(list_str):
    return parseTags(list_str)


def listToString(olist):
    return tagsToString(olist)


def createBookINFO(ID=0, name="", authors=None, pub_date="", publisher="", isbn="", language="", cover_path="",
                   rating=0, file_path="", tags=None, bookLists=None):
    # cover_path, 封面的存储位置，通过此信息加载封面
    # rating, 评分，int型数据，1星到5星，0表示未评分
    # file_path, 文件位置，可以根据此信息打开文件
    # tags, 书籍的标签，列表
    # bookLists, 所属的书单，列表
    if bookLists is None:
        bookLists = []
    if tags is None:
        tags = []
    if authors is None:
        authors = []
    info = {'ID': ID, 'name': name, 'authors': authors, 'pub_data': pub_date, 'publisher': publisher, 'isbn': isbn,
            'language': language, 'cover_path': cover_path, 'rating': rating, 'file_path': file_path, 'tags': tags,
            'bookLists': bookLists}

    return info


# 每次加入一本新书的时候调用该函数，将为该书分配ID，并将该书加入数据库中
def createNewBook(name="", authors=None, pub_date="", publisher="", isbn="", language="", cover_path="",
                  rating=0, file_path="", tags=None, bookLists=None):
    GlobalVar.CUR_ID += 1
    ID = GlobalVar.CUR_ID
    book = Book(ID, name, authors, pub_date, publisher, isbn, language, cover_path, rating, file_path, tags,
                bookLists)
    DataBase.addBook(book)


# 每次新建一个书单时调用该方法
# 新建书单的两种方式：1、通过按钮新建一个空书单 2、通过书籍的右键菜单，添加到书单，如果用户填写的书单不存在，将自动新建一个书单，
# 并将相应的书籍添加进去
def createNewBooklist(name):
    booklist = BookList(name, [])
    DataBase.addBooklist(booklist)


# 不提供主动新建作者的方法

# 新建一个历史搜索
def createNewHistory(time, content):
    history = History(time, content)
    DataBase.addHistory(history)


def parseRetBooks(ret):
    books = []
    for row in ret:
        ID = row[0]
        name = row[1]
        authors = parseListString(row[2])
        pub_date = row[3]
        publisher = row[4]
        isbn = row[5]
        language = row[6]
        cover_path = row[7]
        rating = row[8]
        file_path = row[9]
        tags = parseTags(row[10])
        booklists = parseListString(row[11])
        book = Book(ID, name, authors, pub_date, publisher, isbn, language, cover_path, rating, file_path, tags,
                    booklists)
        books.append(book)
    return books


def parseRetBooklists(ret):
    booklists = []
    for row in ret:
        name = row[0]
        ID = parseListString(row[1])
        booklist = BookList(name, ID)
        booklists.append(booklist)
    return booklists


def parseRetAuthors(ret):
    authors = []
    for row in ret:
        name = row[0]
        books = parseListString(row[1])
        author = Author(name, books)
        authors.append(author)
    return authors
