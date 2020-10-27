# 此文件存储搜索方法
import re


def searchBooks(searchAttr, searchAttrMode, books, keyword):
    if searchAttr == '按书名':
        if searchAttrMode == '准确匹配':
            books = [book for book in books if book.name == keyword]
        elif searchAttrMode == '模糊匹配':
            books = [book for book in books if keyword in book.name]
        else:  # 正则匹配
            books = [book for book in books if re.match(keyword, book.name)]
    elif searchAttr == '按作者':
        if searchAttrMode == '准确匹配':
            books = [book for book in books if keyword in book.authors]
        elif searchAttrMode == '模糊匹配':
            books = [book for book in books if book.hasAnthorFuzzy(keyword)]
        else:  # 正则匹配
            books = [book for book in books if book.hasAuthorRegExp(keyword)]
    elif searchAttr == '按书单':
        if searchAttrMode == '准确匹配':
            books = [book for book in books if keyword in book.bookLists]
        elif searchAttrMode == '模糊匹配':
            books = [book for book in books if book.inBooklistFuzzy(keyword)]
        else:  # 正则匹配
            books = [book for book in books if book.inBooklistRegExp(keyword)]
    elif searchAttr == '按标签':
        if searchAttrMode == '准确匹配':
            books = [book for book in books if keyword in book.authors]
        elif searchAttrMode == '模糊匹配':
            books = [book for book in books if book.hasTagFuzzy(keyword)]
        else:  # 正则匹配
            books = [book for book in books if book.hasTagRegExp(keyword)]
    elif searchAttr == '按出版社':
        if searchAttrMode == '准确匹配':
            books = [book for book in books if book.publisher == keyword]
        elif searchAttrMode == '模糊匹配':
            books = [book for book in books if keyword in book.publisher]
        else:  # 正则匹配
            books = [book for book in books if re.match(keyword, book.publisher)]
    else:  # 按ISBN
        if searchAttrMode == '准确匹配':
            books = [book for book in books if book.isbn == keyword]
        elif searchAttrMode == '模糊匹配':
            books = [book for book in books if keyword in book.isbn]
        else:  # 正则匹配
            books = [book for book in books if re.match(keyword, book.isbn)]
    return books


def highSearchBooks(authors, books, booktag, name, press):
    if name:
        books = [book for book in books if name in book.name]
    if authors:
        for author in authors:
            books = [book for book in books if book.hasAnthorFuzzy(author)]
    if press:
        books = [book for book in books if press in book.publisher]
    if booktag:
        for tag in booktag:
            books = [book for book in books if book.hasTagFuzzy(tag)]
    return books


def searchByTag(ITEM_TEXT, books, item):
    if item.parent().text(0) == "作者":
        books = [book for book in books if ITEM_TEXT in book.authors]
    elif item.parent().text(0) == "书单":
        books = [book for book in books if ITEM_TEXT in book.bookLists]
    elif item.parent().text(0) == "标签":
        books = [book for book in books if ITEM_TEXT in book.tags]
    elif item.parent().text(0) == "语言":
        books = [book for book in books if book.language == ITEM_TEXT]
    elif item.parent().text(0) == "出版社":
        books = [book for book in books if book.publisher == ITEM_TEXT]
    else:  # 评分
        if ITEM_TEXT == "5星":
            books = [book for book in books if book.rating == 5]
        elif ITEM_TEXT == '4星':
            books = [book for book in books if book.rating == 4]
        elif ITEM_TEXT == '3星':
            books = [book for book in books if book.rating == 3]
        elif ITEM_TEXT == '2星':
            books = [book for book in books if book.rating == 2]
        elif ITEM_TEXT == '1星':
            books = [book for book in books if book.rating == 1]
        else:  # 尚未评分
            books = [book for book in books if book.rating == 0]
    return books
