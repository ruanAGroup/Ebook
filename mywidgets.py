import os
import re
from math import ceil
from PyQt5 import QtGui
from PyQt5.QtCore import QSize, Qt, pyqtSignal, QStringListModel
from PyQt5.QtGui import QFont, QIcon, QPixmap, QCursor
from PyQt5.QtWidgets import *
from basic import strListToString
from classes import Book
from typing import List
import heapq
from mydatabase import MyDb
from mydialogs import HighSearchDialog
from search import searchBooks, highSearchBooks, searchByTag

Books = List[Book]


class MyToolBar(QToolBar):
    sortModeChangedSignal = pyqtSignal()
    sendBackMail = pyqtSignal(str)

    def __init__(self):
        super(MyToolBar, self).__init__()
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.addbook = QAction(QIcon('img/add-2.png'), "添加书籍", self)
        self.inbook = QAction(QIcon('img/import-6.png'), "导入文件", self)
        self.editbook = QAction(QIcon('img/edit-5.png'), "编辑元数据", self)

        self.deletebook = QAction(QIcon('img/delete-4.png'), "移除书籍", self)
        self.booklist = QAction(QIcon('img/booklist-2.png'), "创建书单", self)
        self.bookshelf = QAction(QIcon('img/bookshelf.png'), "打开书库", self)
        self.export = QAction(QIcon('img/export-1.png'), "导出信息", self)
        self.star = QAction(QIcon('img/star-1.png'), "支持我们", self)
        self.gethelp = QAction(QIcon("img/help-2.png"), "帮助", self)
        self.setting = QAction(QIcon("img/setting-3.png"), "设置", self)

        self.sortMode = "name"
        self.sortByName = QAction("按书名排序", self)
        self.sortByAuthor = QAction("按作者排序", self)
        self.sortByPublisher = QAction("按出版社排序", self)
        self.sortByPubDate = QAction("按出版时间排序", self)
        self.sortByRating = QAction("按评分排序", self)

        self.sortByName.triggered.connect(lambda: self.changeSortMode("name"))
        self.sortByAuthor.triggered.connect(lambda: self.changeSortMode("author"))
        self.sortByPublisher.triggered.connect(lambda: self.changeSortMode("publisher"))
        self.sortByPubDate.triggered.connect(lambda: self.changeSortMode("pub_date"))
        self.sortByRating.triggered.connect(lambda: self.changeSortMode("rating"))

        self.sortMenu = QMenu()
        self.sortMenu.setFont(QFont("", 14))
        self.sortMenu.addActions([self.sortByName, self.sortByAuthor, self.sortByPublisher, self.sortByPubDate,
                                  self.sortByRating])
        self.sortBtn = QToolButton()
        self.sortBtn.setText("排序")
        self.sortBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.sortBtn.setIcon(QIcon('img/sortUp-2.png'))
        self.sortBtn.setMenu(self.sortMenu)
        self.sortBtn.setPopupMode(QToolButton.MenuButtonPopup)

        self.readInDefault = QAction("在默认pdf阅读器中打开", self)
        self.readInOur = QAction("在我们的简易阅读器中打开", self)
        self.openEditor = QAction("打开我们的简易编辑器", self)

        self.readMenu = QMenu()
        self.readMenu.setFont(QFont("", 14))
        self.readMenu.addActions([self.readInDefault, self.readInOur, self.openEditor])
        self.readbook = QToolButton()
        self.readbook.setText("阅读书籍")
        self.readbook.setIcon(QIcon('img/read-2.png'))
        self.readbook.setMenu(self.readMenu)
        self.readbook.setPopupMode(QToolButton.MenuButtonPopup)
        self.readbook.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.outAsHtml = QAction("导出为HTML", self)
        self.outAsTxt = QAction("导出为TXT", self)
        self.outAsDocx = QAction("导出为docx", self)

        self.outMenu = QMenu()
        self.outMenu.setFont(QFont("", 14))
        self.outMenu.addActions([self.outAsHtml, self.outAsDocx, self.outAsTxt])
        self.outBtn = QToolButton()
        self.outBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.outBtn.setText("格式转换")
        self.outBtn.setMenu(self.outMenu)
        self.outBtn.setIcon(QIcon('img/convert-1.png'))
        self.outBtn.setPopupMode(QToolButton.InstantPopup)

        self.shareMenu = QMenu()
        self.shareMenu.setFont(QFont("", 14))
        self.toKindle = self.shareMenu.addMenu("发送到kindle")
        self.toKindle.setFont(QFont("", 14))
        self.toKindle.triggered.connect(self.menuClicked)
        self.inputEmail = QAction("添加Kindle邮箱", self)
        self.inputEmail.triggered.connect(self.inputMail)
        self.toQQ = self.shareMenu.addMenu("分享到QQ")
        self.toQQ.setFont(QFont("", 14))
        self.toWeChat = self.shareMenu.addMenu("分享到微信")
        self.toWeChat.setFont(QFont("", 14))
        self.toQQByPic = QAction("分享我们的软件", self)
        self.toQQByFile = QAction("分享文件", self)
        self.toWeChatByPic = QAction("分享我们的软件", self)
        self.toWeChatByFile = QAction("分享文件", self)
        self.toQQ.addActions([self.toQQByFile, self.toQQByPic])
        self.toWeChat.addActions([self.toWeChatByFile, self.toWeChatByPic])
        self.shareBtn = QToolButton()
        self.shareBtn.setIcon(QIcon('img/share-7.png'))
        self.shareBtn.setText("分享")
        self.shareBtn.setMenu(self.shareMenu)
        self.shareBtn.setPopupMode(QToolButton.InstantPopup)
        self.shareBtn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        self.addActions([self.addbook, self.inbook])
        self.addSeparator()
        self.addActions([self.editbook])
        self.addWidget(self.sortBtn)
        self.addSeparator()
        self.addWidget(self.readbook)
        self.addWidget(self.outBtn)
        self.addActions([self.deletebook])
        self.addSeparator()
        self.addActions([self.booklist, self.bookshelf])
        self.addSeparator()
        self.addActions([self.export])
        self.addWidget(self.shareBtn)
        self.addActions([self.star])
        self.addSeparator()
        self.addActions([self.setting])

    def setTSize(self, TSize):
        if TSize == "小":
            # self.setMinimumSize(QSize(100, 100))
            self.setIconSize(QSize(50, 50))
            self.setFont(QFont("", 13))
        elif TSize == '中':
            # self.setMinimumSize(QSize(150, 150))
            self.setIconSize(QSize(70, 70))
            self.setFont(QFont("", 14))
        else:
            # self.setMinimumSize(QSize(200, 200))
            self.setIconSize(QSize(100, 100))
            self.setFont(QFont("", 15))

    def changeSortMode(self, attr: str):
        self.sortMode = attr
        self.sortModeChangedSignal.emit()

    def inputMail(self):
        mail, ok = QInputDialog.getText(self, "输入邮箱", "请输入邮箱")
        if ok:
            pat = re.compile(r'^[A-Za-z\d]+([-_.][A-Za-z\d]+)*@([A-Za-z\d]+[-.])+[A-Za-z\d]{2,4}$')
            if pat.match(mail):
                self.sendMail(mail)
            else:
                QMessageBox.about(self, "提醒", "请输入合法邮箱")

    def updateKindleEmail(self, emails):
        self.toKindle.clear()
        for mail in emails:
            action = QAction(mail, self)
            self.toKindle.addAction(action)
        self.toKindle.addAction(self.inputEmail)
        # self.toKindle.triggered.connect(self.menuClicked)

    def menuClicked(self, action):
        if action.text() != "添加Kindle邮箱":
            self.sendMail(action.text())

    def sendMail(self, mail):
        if mail:
            self.sendBackMail.emit(mail)


class MyTree(QTreeWidget):
    itemClickedSignal = pyqtSignal(list)

    def __init__(self, db: MyDb):
        super(MyTree, self).__init__()
        self.db = db
        self.setColumnCount(1)
        self.setHeaderHidden(True)
        self.authors = QTreeWidgetItem(self)
        self.authors.setText(0, "作者")
        self.authors.setIcon(0, QIcon('img/author-1.png'))
        self.booklists = QTreeWidgetItem(self)
        self.booklists.setText(0, "书单")
        self.booklists.setIcon(0, QIcon('img/list-1.png'))
        self.tags = QTreeWidgetItem(self)
        self.tags.setText(0, "标签")
        self.tags.setIcon(0, QIcon('img/tag-1.png'))
        self.language = QTreeWidgetItem(self)
        self.language.setText(0, "语言")
        self.language.setIcon(0, QIcon('img/language-3.png'))
        self.publisher = QTreeWidgetItem(self)
        self.publisher.setText(0, "出版社")
        self.publisher.setIcon(0, QIcon("img/publish-1.png"))
        self.rating = QTreeWidgetItem(self)
        self.rating.setText(0, "评分")
        self.rating.setIcon(0, QIcon('img/rate-3.png'))
        self.fiveScore = QTreeWidgetItem(self.rating)
        self.fiveScore.setText(0, "5星")
        self.fourScore = QTreeWidgetItem(self.rating)
        self.fourScore.setText(0, "4星")
        self.threeScore = QTreeWidgetItem(self.rating)
        self.threeScore.setText(0, "3星")
        self.twoScore = QTreeWidgetItem(self.rating)
        self.twoScore.setText(0, "2星")
        self.oneScore = QTreeWidgetItem(self.rating)
        self.oneScore.setText(0, "1星")
        self.noScore = QTreeWidgetItem(self.rating)
        self.noScore.setText(0, "尚未评分")
        self.itemClicked.connect(self.onItemClicked)

    def setTSize(self, TSize):
        if TSize == "小":
            self.setFont(QFont("", 13))
            self.setIconSize(QSize(30, 30))
        elif TSize == '中':
            self.setFont(QFont("", 14))
            self.setIconSize(QSize(40, 40))
        else:
            self.setFont(QFont("", 15))
            self.setIconSize(QSize(50, 50))

    def updateAuthors(self, author_list):
        self.authors.takeChildren()
        for author in author_list:
            node = QTreeWidgetItem(self.authors)
            node.setText(0, author)

    def updateBookLists(self, book_lists):
        self.booklists.takeChildren()
        for booklist in book_lists:
            node = QTreeWidgetItem(self.booklists)
            node.setText(0, booklist)

    def updateTags(self, tag_list):
        self.tags.takeChildren()
        for tag in tag_list:
            node = QTreeWidgetItem(self.tags)
            node.setText(0, tag)

    def updateLanguage(self, language_list):
        self.language.takeChildren()
        for language in language_list:
            node = QTreeWidgetItem(self.language)
            node.setText(0, language)

    def updatePublisher(self, pub_list):
        self.publisher.takeChildren()
        for publisher in pub_list:
            node = QTreeWidgetItem(self.publisher)
            node.setText(0, publisher)

    def onItemClicked(self, item: QTreeWidgetItem, col):
        books = self.db.getAllBooks()
        ITEM_TEXT = item.text(0)
        if item.parent():
            books = searchByTag(ITEM_TEXT, books, item)
        self.itemClickedSignal.emit(books)


class MyLabel(QLabel):
    clicked = pyqtSignal()

    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        self.clicked.emit()
        super(MyLabel, self).mousePressEvent(ev)


class MenuLabel(QLabel):
    clicked = pyqtSignal()
    editDataSignal = pyqtSignal()
    sendKindleSignal = pyqtSignal(str)
    addTagSignal = pyqtSignal(str)
    addToBooklistSignal = pyqtSignal(str)
    changeCoverSignal = pyqtSignal()

    def __init__(self, db, bookID, *args):
        super(MenuLabel, self).__init__(*args)
        self.db = db
        self.bookID = bookID
        self.menu = QMenu()
        editData = QAction("编辑元数据", self.menu)
        editData.triggered.connect(self.onEditData)
        changeCover = QAction("更换封面", self.menu)
        changeCover.triggered.connect(self.onChangeCover)
        self.menu.addActions([editData, changeCover])
        self.addTag = self.menu.addMenu("添加标签")
        self.addToBookList = self.menu.addMenu("添加到书单")
        self.sendToKindle = self.menu.addMenu("发送到Kindle")
        self.inputEmail = QAction("添加Kindle邮箱", self)
        self.inputEmail.triggered.connect(self.inputMail)
        self.sendToKindle.triggered.connect(self.onSendKindle)
        self.addTag.triggered.connect(self.onAddTag)
        self.addToBookList.triggered.connect(self.onAddToBooklist)
        # addToBookList = QAction("添加到书单", self.menu)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)

    def onChangeCover(self):
        self.changeCoverSignal.emit()

    def onAddTag(self, action):
        self.addTagSignal.emit(action.text())

    def onAddToBooklist(self, action):
        self.addToBooklistSignal.emit(action.text())

    def inputMail(self):
        mail, ok = QInputDialog.getText(QInputDialog(), "输入邮箱", "请输入邮箱")
        if ok:
            pat = re.compile(r'^[A-Za-z\d]+([-_.][A-Za-z\d]+)*@([A-Za-z\d]+[-.])+[A-Za-z\d]{2,4}$')
            if pat.match(mail):
                self.sendMail(mail)
            else:
                QMessageBox.about(self, "提醒", "请输入合法邮箱")

    def sendMail(self, mail):
        self.sendKindleSignal.emit(mail)

    def onSendKindle(self, action):
        if action.text() != '添加Kindle邮箱':
            self.sendMail(action.text())

    def generateAddTagMenu(self):
        self.addTag.clear()
        tags = self.db.getAllTags()
        book = self.db.getBookByID(self.bookID)
        tags -= set(book.tags)
        for tag in tags:
            action = QAction(tag, self)
            self.addTag.addAction(action)

    def generateAddToBookListMenu(self):
        self.addToBookList.clear()
        booklists = {booklist.name for booklist in self.db.getAllBookLists()}
        book = self.db.getBookByID(self.bookID)
        booklists -= set(book.bookLists)
        for booklist in booklists:
            action = QAction(booklist, self)
            self.addToBookList.addAction(action)

    def generateSendToKindleMenu(self):
        self.sendToKindle.clear()
        self.sendToKindle.addAction(self.inputEmail)
        mails = self.db.getAllKindleMail()
        for mail in mails:
            action = QAction(mail, self)
            self.sendToKindle.addAction(action)

    def generateContextMenu(self):
        self.generateAddTagMenu()
        self.generateAddToBookListMenu()
        self.generateSendToKindleMenu()

    def showContextMenu(self, point):
        if self.underMouse():
            self.generateContextMenu()
            self.menu.exec_(QCursor.pos())

    def onEditData(self):
        self.editDataSignal.emit()

    def mousePressEvent(self, ev):
        self.clicked.emit()
        super(MenuLabel, self).mousePressEvent(ev)


class MyGrid(QGridLayout):
    itemClicked = pyqtSignal(int)
    editDataSignal = pyqtSignal()
    sendToKindleSignal = pyqtSignal(str)
    addTagSignal = pyqtSignal(str)
    addToBooklistSignal = pyqtSignal(str)
    changeCoverSignal = pyqtSignal()

    def __init__(self, parent, scro, db):
        super(MyGrid, self).__init__(parent)
        self.db = db
        self.father = parent
        self.scrollarea = scro
        self.setSpacing(30)
        self.lastActive = None
        self.dict = {}
        self.itemWidth = 365
        self.itemHeight = 458

    def updateView(self, books: Books):
        self.deleteAll()
        self.lastActive = None
        if not books:
            return
        total = len(books)
        cols = 3
        rows = ceil(total / cols)
        points = [(i, j) for i in range(rows) for j in range(cols)]
        tempWid = QWidget()
        for point, book in zip(points, books):
            tempLabel = MenuLabel(self.db, book.ID)
            tempLabel.changeCoverSignal.connect(self.onChangeCover)
            tempLabel.addTagSignal.connect(self.onAddTag)
            tempLabel.addToBooklistSignal.connect(self.onAddToBooklist)
            tempLabel.sendKindleSignal.connect(self.onToKindle)
            tempLabel.editDataSignal.connect(self.onEditData)
            tempLabel.setPixmap(QPixmap(book.cover_path).scaled(self.itemWidth, self.itemHeight))
            tempLabel.setScaledContents(True)
            if book.name:
                tempLabel.setToolTip("书名: " + book.name + '\n' + "作者: " + strListToString(book.authors))
            tempLabel.clicked.connect(self.onItemClicked)
            self.dict[tempLabel] = book.ID
            self.addWidget(tempLabel, *point)
        tempWid.setLayout(self)
        self.scrollarea.setWidget(tempWid)
        self.father = tempWid

    def onChangeCover(self):
        self.changeCoverSignal.emit()

    def onAddTag(self, tag):
        self.addTagSignal.emit(tag)

    def onToKindle(self, address):
        self.sendToKindleSignal.emit(address)

    def onAddToBooklist(self, name):
        self.addToBooklistSignal.emit(name)

    def onEditData(self):
        self.editDataSignal.emit()

    def deleteAll(self):
        while self.count():
            item = self.takeAt(0)
            widget = item.widget()
            widget.deleteLater()

    def onItemClicked(self):
        sender = self.sender()
        if self.lastActive:
            self.lastActive.setStyleSheet("")
        sender.setStyleSheet("border:4px solid blue;")
        self.lastActive = sender
        self.itemClicked.emit(self.dict[sender])  # 传回一个ID


class MyList(QVBoxLayout):
    def __init__(self, father, TSize):
        super(MyList, self).__init__(father)
        self.TSize = TSize
        self.father = father
        self.picLabel = QLabel()
        self.picLabel.setPixmap(QPixmap('img/default-pic.png').scaled(365, 458))
        self.namelabel = QLabel("书名")
        self.authorlabel = QLabel("作者")
        self.pathlabel = QLabel("路径")
        self.formatlabel = QLabel("格式")
        self.tagslabel = QLabel("标签")
        self.booklistslabel = QLabel("书单")
        self.name = QLabel("未知")
        self.authors = QLabel("未知")
        self.path = MyLabel("无")
        self.format = MyLabel("无")
        self.tags = QLabel("无")
        self.booklists = QLabel("无")
        self.bookPath = None

        self.form = QFormLayout()
        self.form.insertRow(0, self.namelabel, self.name)
        self.form.insertRow(1, self.authorlabel, self.authors)
        self.form.insertRow(2, self.pathlabel, self.path)
        self.form.insertRow(3, self.formatlabel, self.format)
        self.form.insertRow(4, self.tagslabel, self.tags)
        self.form.insertRow(5, self.booklistslabel, self.booklists)

        self.addWidget(self.picLabel)
        temwidget = QWidget()
        temwidget.setFont(QFont("", self.getSize()))
        temwidget.setLayout(self.form)
        self.scrollarea = QScrollArea()
        self.scrollarea.setFrameShape(QFrame.NoFrame)
        self.scrollarea.setWidget(temwidget)
        self.addWidget(self.scrollarea)

    def setTSize(self, TSize):
        self.TSize = TSize

    def getSize(self):
        if self.TSize == '大':
            return 14
        elif self.TSize == '中':
            return 13
        else:
            return 12

    def updateView(self, book: Book):
        if book.cover_path:
            self.picLabel.setPixmap(QPixmap(book.cover_path).scaled(365, 458))
        else:
            self.picLabel.setPixmap(QPixmap('img/default-pic.png').scaled(365, 458))
        if book.name:
            self.name.setText(book.name)
        else:
            self.name.setText("未知")
        if book.authors:
            self.authors.setText(strListToString(book.authors))
        else:
            self.authors.setText("未知")
        if book.file_path:
            self.bookPath = book.file_path
            self.path.setText("<a style='color: blue'>打开</a>")
            self.format.setText("<a style='color: blue'>PDF</a>")
            self.format.clicked.connect(self.openFile)
            self.path.clicked.connect(self.openPath)
        else:
            self.bookPath = None
            self.path.setText("无")
            self.format.setText("无")
        if book.tags:
            self.tags.setText(strListToString(book.tags))
        else:
            self.tags.setText("无")
        if book.bookLists:
            self.booklists.setText(strListToString(book.bookLists))
        else:
            self.booklists.setText("无")
        temp = QWidget()
        temp.setFont(QFont("", self.getSize()))
        temp.setLayout(self.form)
        self.scrollarea.setWidget(temp)

    def openFile(self):
        if not self.bookPath:
            return
        if os.path.exists(self.bookPath):
            os.startfile(self.bookPath)
        else:
            QMessageBox.about(self, "提醒", "文件不存在")

    def openPath(self):
        if not self.bookPath:
            return
        mypath, fileName = os.path.split(self.bookPath)
        if os.path.exists(mypath):
            os.startfile(mypath)
        else:
            QMessageBox.about(self, "提醒", "路径不存在")


class MySearch(QToolBar):
    updateBookViewSignal = pyqtSignal(list)

    def __init__(self, db: MyDb):
        super(MySearch, self).__init__()
        self.db = db
        self.setFont(QFont("", 15))
        self.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.searchModeLabel = QLabel("搜索模式")
        self.searchBy = QComboBox()
        self.searchBy.addItems(['按书名', '按作者', '按书单', '按标签', '按出版社', '按ISBN'])
        self.searchAttr = self.searchBy.currentText()
        self.searchBy.currentTextChanged.connect(self.changeAttr)
        self.searchMode = QComboBox()
        self.searchMode.addItems(['准确匹配', '模糊匹配', '正则匹配'])
        self.searchAttrMode = self.searchMode.currentText()
        self.searchMode.currentTextChanged.connect(self.changeAttrMode)
        self.inputLine = QLineEdit()
        self.inputLine.returnPressed.connect(self.onSearch)  # 开始搜索
        self.inputCompleter = QCompleter()

        # 初始化
        model = QStringListModel()
        booknames = self.db.getAllBookNames()
        model.setStringList(booknames)
        self.inputCompleter.setModel(model)
        self.inputCompleter.setFilterMode(Qt.MatchExactly)
        self.inputLine.setCompleter(self.inputCompleter)
        self.inputCompleter.popup().setFont(QFont("", 14))
        self.inputLine.setPlaceholderText("选择搜索模式后，在此输入关键词")
        self.searchAct = QAction(QIcon("img/search-4.png"), "搜索", self)
        self.highSearchAct = QAction(QIcon('img/hsearch-1.png'), "高级搜索", self)
        self.historyMenu = QMenu()
        self.historyMenu.triggered.connect(self.historyClicked)
        self.historyMenu.setFont(QFont("", 14))
        self.historyBtn = QToolButton()
        self.historyBtn.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.historyBtn.setText("历史搜索")
        self.historyBtn.setMenu(self.historyMenu)
        self.historyBtn.setIcon(QIcon('img/history-1.png'))
        self.historyBtn.setPopupMode(QToolButton.InstantPopup)
        self.updateHistory()

        self.searchAct.triggered.connect(self.onSearch)
        self.highSearchAct.triggered.connect(self.onHighSearch)

        self.addWidget(self.searchModeLabel)
        self.addWidget(self.searchBy)
        self.addWidget(self.searchMode)
        self.addSeparator()
        self.addWidget(self.inputLine)
        self.addAction(self.searchAct)
        self.addSeparator()
        self.addActions([self.highSearchAct])
        self.addWidget(self.historyBtn)

    def onSearch(self):
        books = self.db.getAllBooks()
        keyword = self.inputLine.text()
        if keyword:
            self.db.addAHistory(keyword)
            self.updateHistory()
            books = searchBooks(self.searchAttr, self.searchAttrMode, books, keyword)
        self.updateBookViewSignal.emit(books)

    def onHighSearch(self):
        dig = HighSearchDialog(self)
        dig.finishSignal.connect(self.handleHigh)
        dig.show()

    def handleHigh(self, name, authors, press, booktag):  # 默认为模糊匹配
        books = self.db.getAllBooks()
        books = highSearchBooks(authors, books, booktag, name, press)
        self.updateBookViewSignal.emit(books)

    def updateHistory(self):
        self.historyMenu.clear()
        histories = self.db.getAllHistory()
        recentTen = heapq.nlargest(10, histories)
        for his in recentTen:
            t, content = his
            action = QAction(content, self.historyMenu)
            self.historyMenu.addAction(action)
        # self.historyMenu.triggered.connect(self.historyClicked)

    def historyClicked(self, action):
        self.inputLine.setText(action.text())

    def changeAttr(self, attr):
        self.searchBy.setCurrentText(attr)
        self.searchAttr = attr
        model = QStringListModel()
        if attr == '按书名':
            booknames = self.db.getAllBookNames()
            model.setStringList(booknames)
        elif attr == '按作者':
            authors = {author.name for author in self.db.getAllAuthors()}
            model.setStringList(authors)
        elif attr == '按书单':
            booklists = {booklist.name for booklist in self.db.getAllBookLists()}
            model.setStringList(booklists)
        elif attr == '按标签':
            tags = self.db.getAllTags()
            model.setStringList(tags)
        elif attr == '按出版社':
            publishers = self.db.getAllPublishers()
            model.setStringList(publishers)
        else:  # 按ISBN
            isbns = self.db.getAllISBNs()
            model.setStringList(isbns)
        self.inputCompleter.setModel(model)

    def changeAttrMode(self, attrMode):
        self.searchMode.setCurrentText(attrMode)
        self.searchAttrMode = attrMode
        if attrMode == '准确匹配':
            self.inputCompleter.setFilterMode(Qt.MatchExactly)
        elif attrMode == '模糊匹配':
            self.inputCompleter.setFilterMode(Qt.MatchContains)
