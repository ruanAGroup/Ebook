# 此文件为UI程序
from functools import partial

from PyQt5.QtGui import *
from mywidgets import *
from mydialogs import *
from mythreads import *
from basic import *
from settings import storeSetting


class BookManager(QMainWindow):
    def __init__(self, setting, setting_filename):
        super(BookManager, self).__init__()
        self.setting_filename = setting_filename
        self.setting = setting
        self.toolbar = MyToolBar()
        self.toolbar.setTSize(self.setting["toolbarSize"])
        self.addToolBar(self.toolbar)
        self.generateToolBar()

        self.mainExePath = os.getcwd()
        self.db = MyDb(os.path.join(self.mainExePath, 'info.db'))
        if not os.path.exists('books'):
            os.mkdir('books')
        self.bookShelfPath = os.path.join(self.mainExePath, "books")
        self.pdfReaderName = 'main'
        self.editorName = 'editor'

        self.searchLine = MySearch(self.db)
        self.setSearch()
        self.treeView = MyTree(self.db)
        self.treeView.setTSize(self.setting['treeSize'])
        self.treeView.itemClickedSignal.connect(self.onTreeItemClicked)
        self.treeView.setMaximumWidth(1000)
        self.treeView.setMinimumWidth(200)
        self.scrollarea = QScrollArea()
        tempwidget = QWidget()
        # tempwidget.setStyleSheet("QLabel{border:2px solid red;}")
        self.booksView = MyGrid(tempwidget, self.scrollarea, self.db)
        self.generateBookView()
        tempinfo = QWidget()
        # tempinfo.setMinimumWidth(0)
        self.infoView = MyList(tempinfo, self.setting['bookInfoSize'])

        self.scrollarea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollarea.setMinimumWidth(1190)
        self.scrollarea.setMaximumWidth(1800)
        self.scrollarea.setWidget(tempwidget)
        tempinfo.setLayout(self.infoView)
        splitter1 = QSplitter(Qt.Horizontal)
        splitter1.addWidget(self.scrollarea)
        splitter1.addWidget(tempinfo)
        splitter1.setSizes([1000, 400])
        splitter2 = QSplitter(Qt.Horizontal)
        splitter2.addWidget(self.treeView)
        splitter2.addWidget(splitter1)
        splitter2.setSizes([400, 1400])

        self.VBox = QVBoxLayout()
        self.VBox.addWidget(self.searchLine)
        self.VBox.addWidget(splitter2)
        self.mainwidget = QWidget()
        self.mainwidget.setLayout(self.VBox)
        self.setCentralWidget(self.mainwidget)

        # 打开时读取数据
        self.curShowBooks = self.db.getAllBooks()
        # print("Hello")
        os.chdir(self.mainExePath)
        self.booksView.updateView(self.curShowBooks)
        self.updateTreeView()
        emails = self.db.getAllKindleMail()
        self.toolbar.updateKindleEmail(emails)
        self.searchLine.updateBookViewSignal.connect(self.updateBySearch)
        # time.sleep(1)

        QToolTip.setFont(QFont("", 14))
        self.setWindowTitle("图书管理系统")
        self.setWindowIcon(QIcon('img/icon-2.png'))
        self.showMaximized()
        self.show()

    def generateBookView(self):
        self.booksView.itemClicked.connect(self.updateInfo)
        self.booksView.editDataSignal.connect(self.editBook)
        self.booksView.sendToKindleSignal.connect(self.sendMail)
        self.booksView.addTagSignal.connect(self.addTag)
        self.booksView.addToBooklistSignal.connect(self.addBookListByBooksView)
        self.booksView.changeCoverSignal.connect(self.onChangeCover)

    def generateToolBar(self):
        self.toolbar.addbook.triggered.connect(self.addBook)
        self.toolbar.inbook.triggered.connect(self.inBook)
        self.toolbar.editbook.triggered.connect(self.editBook)
        self.toolbar.sortBtn.clicked.connect(self.sortBooks)
        # self.toolbar.highSort.triggered.connect(self.HighSort)
        self.toolbar.readbook.clicked.connect(self.readBook)
        self.toolbar.readInDefault.triggered.connect(self.readBook)
        self.toolbar.readInOur.triggered.connect(self.readBookInOur)
        self.toolbar.openEditor.triggered.connect(self.openEditor)
        self.toolbar.outAsTxt.triggered.connect(self.outAsTxt)
        self.toolbar.outAsDocx.triggered.connect(self.outAsDocx)
        self.toolbar.outAsHtml.triggered.connect(self.outAsHtml)
        self.toolbar.deletebook.triggered.connect(self.deleteBook)
        self.toolbar.booklist.triggered.connect(self.addBookList)
        self.toolbar.bookshelf.triggered.connect(self.openBookShelf)
        self.toolbar.export.triggered.connect(self.export)
        # self.toolbar.share.triggered.connect(self.share)
        self.toolbar.toQQByFile.triggered.connect(self.toQQByFile)
        self.toolbar.toQQByPic.triggered.connect(self.toQQByPic)
        self.toolbar.toWeChatByFile.triggered.connect(self.toWeChatByFile)
        self.toolbar.toWeChatByPic.triggered.connect(self.toWeChatByPic)
        self.toolbar.star.triggered.connect(self.giveusStar)
        # self.toolbar.gethelp.triggered.connect(self.getHelp)
        self.toolbar.setting.triggered.connect(self.setSetting)
        self.toolbar.sortModeChangedSignal.connect(self.sortBooks)
        self.toolbar.sendBackMail.connect(self.sendMail)

    def addBookListByBooksView(self, booklistname):
        book = self.getCurrentBook()
        book.addToList(self.db, booklistname)
        book.updateDB(self.db)
        self.updateTreeView()
        if self.booksView.lastActive:
            self.updateInfo(self.booksView.dict[self.booksView.lastActive])
        self.searchLine.changeAttr(self.searchLine.searchAttr)

    def getCurrentBook(self):
        if self.booksView.lastActive:
            return self.db.getBookByID(self.booksView.dict[self.booksView.lastActive])
        else:
            return None

    def addTag(self, tag):
        book = self.getCurrentBook()
        book.tags.append(tag)
        book.updateDB(self.db)
        self.updateInfo(self.booksView.dict[self.booksView.lastActive])

    def addBook(self):
        os.chdir(self.mainExePath)
        filename, _ = QFileDialog.getOpenFileName(self, "选择文件", ".", "PDF file(*.pdf)")
        if filename:
            doc = fitz.open(filename)
            name = getTitle(doc)
            authors = getAuthors(doc)
            pub_date = getPubDate(doc)
            book_path, file_path = getFilePath(self.bookShelfPath, name, self.db.getID(), filename)
            if not book_path:
                return
            cover_path = getCover(doc, book_path)
            self.db.createNewBook(name, authors, pub_date, file_path=file_path, cover_path=cover_path)
            # print("Hi")
            self.curShowBooks = self.db.getAllBooks()
            # print("Hello")
            os.chdir(self.mainExePath)
            self.booksView.updateView(self.curShowBooks)
            self.updateTreeView()

    def updateInfo(self, ID):
        book = self.db.getBookByID(ID)
        # print(ID)
        self.infoView.updateView(book)

    def updateTreeView(self):
        authors = {author.name for author in self.db.getAllAuthors()}
        self.treeView.updateAuthors(authors)
        booklists = {booklist.name for booklist in self.db.getAllBookLists()}
        self.treeView.updateBookLists(booklists)
        tags = self.db.getAllTags()
        self.treeView.updateTags(tags)
        languages = self.db.getAllLanguages()
        # print(languages)
        # print("Lan", languages)
        self.treeView.updateLanguage(languages)
        publishers = self.db.getAllPublishers()
        # print("Pub", publishers)
        # print(publishers)
        self.treeView.updatePublisher(publishers)

    def onTreeItemClicked(self, books):
        self.curShowBooks = books
        self.booksView.updateView(books)

    def inBook(self):
        dig = ImportFileDialog(self.bookShelfPath, self.db, self)
        dig.finishSignal.connect(self.onInBook)
        # self.importfiledialog.show()

    def onInBook(self, pdfFilePath, name, authors, language, rating):
        doc = fitz.open(pdfFilePath)
        book_path, _ = os.path.split(pdfFilePath)
        cover_path = getCover(doc, book_path)
        self.db.createNewBook(name=name, authors=authors, language=language, rating=rating, file_path=pdfFilePath,
                              cover_path=cover_path)
        self.curShowBooks = self.db.getAllBooks()
        # print("Hello")
        os.chdir(self.mainExePath)
        self.booksView.updateView(self.curShowBooks)
        self.updateTreeView()
        # self.importfiledialog.close()

    def editBook(self):
        if not self.booksView.lastActive:
            self.noteChoseFile()
            return
        book = self.getCurrentBook()
        if book:
            dig = EditDataDialog(self.db, book, self)
            dig.changeSignal.connect(self.onDataChanged)
            dig.show()

    def onChangeCover(self):
        book = self.getCurrentBook()
        dig = changeCoverDialog(book, self)
        dig.coverChangeSignal.connect(self.changeCover)
        dig.show()

    def changeCover(self, pic: QPixmap):
        book = self.getCurrentBook()
        pic.save(book.cover_path)
        self.infoView.updateView(book)
        self.booksView.updateView(self.curShowBooks)

    def onDataChanged(self, ID):
        self.updateTreeView()
        self.updateInfo(ID)
        self.searchLine.changeAttr(self.searchLine.searchAttr)

    def sortBooks(self):
        if self.toolbar.sortMode == 'name':
            books = sorted(self.curShowBooks, key=lambda book: book.name)
            if books == self.curShowBooks:
                self.toolbar.sortBtn.setIcon(QIcon(os.path.join(self.mainExePath, 'img/sortUp-2.png')))
                self.curShowBooks = sorted(self.curShowBooks, key=lambda book: book.name, reverse=True)
            else:
                self.toolbar.sortBtn.setIcon(QIcon(os.path.join(self.mainExePath, 'img/sortDown.png')))
                self.curShowBooks = books
        elif self.toolbar.sortMode == 'author':
            books = sorted(self.curShowBooks, key=lambda book: strListToString(book.authors))
            if books == self.curShowBooks:
                self.toolbar.sortBtn.setIcon(QIcon(os.path.join(self.mainExePath, 'img/sortUp-2.png')))
                self.curShowBooks = sorted(self.curShowBooks, key=lambda book: strListToString(book.authors),
                                           reverse=True)
            else:
                self.toolbar.sortBtn.setIcon(QIcon(os.path.join(self.mainExePath, 'img/sortDown.png')))
                self.curShowBooks = books
        elif self.toolbar.sortMode == 'publisher':
            books = sorted(self.curShowBooks, key=lambda book: book.publisher)
            if books == self.curShowBooks:
                self.toolbar.sortBtn.setIcon(QIcon(os.path.join(self.mainExePath, 'img/sortUp-2.png')))
                self.curShowBooks = sorted(self.curShowBooks, key=lambda book: book.publisher, reverse=True)
            else:
                self.toolbar.sortBtn.setIcon(QIcon(os.path.join(self.mainExePath, 'img/sortDown.png')))
                self.curShowBooks = books
        elif self.toolbar.sortMode == 'pub_date':
            books = sorted(self.curShowBooks, key=lambda book: book.pub_date)
            if books == self.curShowBooks:
                self.toolbar.sortBtn.setIcon(QIcon(os.path.join(self.mainExePath, 'img/sortUp-2.png')))
                self.curShowBooks = sorted(self.curShowBooks, key=lambda book: book.pub_date, reverse=True)
            else:
                self.toolbar.sortBtn.setIcon(QIcon(os.path.join(self.mainExePath, 'img/sortDown.png')))
                self.curShowBooks = books
        else:  # sort by rating
            books = sorted(self.curShowBooks, key=lambda book: book.rating)
            if books == self.curShowBooks:
                self.toolbar.sortBtn.setIcon(QIcon(os.path.join(self.mainExePath, 'img/sortUp-2.png')))
                self.curShowBooks = sorted(self.curShowBooks, key=lambda book: book.rating, reverse=True)
            else:
                self.toolbar.sortBtn.setIcon(QIcon(os.path.join(self.mainExePath, 'img/sortDown.png')))
                self.curShowBooks = books
        self.booksView.updateView(self.curShowBooks)

    def readBook(self):
        if self.booksView.lastActive:
            book = self.getCurrentBook()
            os.startfile(book.file_path)

    def readBookInOur(self):
        if self.booksView.lastActive:
            book = self.getCurrentBook()
            try:
                os.chdir('reader')
                os.system('{} {}'.format(self.pdfReaderName, book.file_path))
                os.chdir('..')
            except Exception:
                print('fail to open')
        else:
            self.noteChoseFile()

    def openEditor(self):
        try:
            os.chdir('editor')
            os.system('{}'.format(self.editorName))
            os.chdir('..')
        except Exception:
            pass

    def outAsTxt(self):
        if self.booksView.lastActive:
            saveFileName, _ = QFileDialog.getSaveFileName(self, "保存文件", ".", "txt file(*.txt)")
            if saveFileName:
                book = self.getCurrentBook()
                t = convertThread(pdfToHtmlorTxt, (book.file_path, saveFileName, "text"))
                t.finishSignal.connect(lambda: self.onFinishOut(saveFileName))
                t.start()
                time.sleep(1)
        else:
            self.noteChoseFile()

    def outAsHtml(self):
        if self.booksView.lastActive:
            saveFileName, _ = QFileDialog.getSaveFileName(self, "保存文件", ".", "html file(*.html)")
            if saveFileName:
                book = self.getCurrentBook()
                t = convertThread(pdfToHtmlorTxt, (book.file_path, saveFileName, "html"))
                t.finishSignal.connect(lambda: self.onFinishOut(saveFileName))
                t.start()
                time.sleep(1)
        else:
            self.noteChoseFile()

    def outAsDocx(self):
        if self.booksView.lastActive:
            saveFileName, _ = QFileDialog.getSaveFileName(self, "保存文件", ".", "docx file(*.docx)")
            if saveFileName:
                book = self.getCurrentBook()
                t = convertThread(pdfToDocx, (book.file_path, saveFileName))
                t.finishSignal.connect(lambda: self.onFinishOut(saveFileName))
                t.start()
                time.sleep(1)
        else:
            self.noteChoseFile()

    def onFinishOut(self, savefileName):
        ret = QMessageBox.question(self, '提示', "转换成功，是否打开文件", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if ret == QMessageBox.Yes:
            os.startfile(savefileName)

    def deleteBook(self):
        if self.booksView.lastActive:
            box = QMessageBox(QMessageBox.Question, "注意", "您确定要从库中移除此文件吗？")
            yes = box.addButton("确定", QMessageBox.YesRole)
            no = box.addButton("取消", QMessageBox.NoRole)
            box.exec_()
            if box.clickedButton() == no:
                return
            elif box.clickedButton() == yes:
                book = self.getCurrentBook()
                book.delete(self.db)
                self.updateTreeView()
                self.curShowBooks = self.db.getAllBooks()
                self.booksView.updateView(self.curShowBooks)
                tempbook = Book()
                self.infoView.updateView(tempbook)
        else:
            self.noteChoseFile()

    def updateBySearch(self, books):
        self.curShowBooks = books
        self.booksView.updateView(self.curShowBooks)

    def addBookList(self):
        dig = CreateBookListDialog(self)
        dig.finishSignal.connect(self.onAddBookList)
        bookname_ids = self.db.getAllBookNameIDs()
        dig.input2.addItems(bookname_ids)
        dig.show()

    def onAddBookList(self, booklistname, bookIds):
        for ID in bookIds:
            book = self.db.getBookByID(ID)
            book.addToList(self.db, booklistname)
            book.updateDB(self.db)
        self.updateTreeView()
        if self.booksView.lastActive:
            self.updateInfo(self.booksView.dict[self.booksView.lastActive])
        else:
            self.noteChoseFile()
        self.searchLine.changeAttr(self.searchLine.searchAttr)

    def openBookShelf(self):
        os.startfile(self.bookShelfPath)

    def export(self):
        dig = ExportINFODialog(self.db, self)
        dig.finishSignal.connect(self.finishExport)

    def finishExport(self, filename):
        ret = QMessageBox.question(self, '提示', "导出完成，是否打开文件", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if ret == QMessageBox.Yes:
            os.startfile(filename)

    def sendMail(self, mail):
        if not self.db.mailInDB(mail):
            self.db.addKindleMail(mail)
            allmails = self.db.getAllKindleMail()
            self.toolbar.updateKindleEmail(allmails)
        if not self.booksView.lastActive:
            self.noteChoseFile()
            return
        book = self.getCurrentBook()
        t = EmailThread(email_to, (book.file_path, mail))
        t.finishSignal.connect(self.finish_mail)
        t.start()
        time.sleep(0.8)

    def finish_mail(self, success):
        if success:
            QMessageBox.about(self, "提示", "发送成功")
        else:
            QMessageBox.about(self, "提示", "抱歉，发送失败，请检查邮箱后再次发送")

    def toQQByFile(self):
        if self.booksView.lastActive:
            book = self.getCurrentBook()
            copyFile(book.file_path)
            QMessageBox.about(self, "提示", "文件已复制到剪贴板")
            CtrlAltZ()
        else:
            self.noteChoseFile()

    def toQQByPic(self):
        if self.booksView.lastActive:
            book = self.getCurrentBook()
            dig = shareByPicDialog(book, self)
            dig.copySignal.connect(self.qqPicCopied)
            dig.show()
        else:
            self.noteChoseFile()

    def noteChoseFile(self):
        QMessageBox.about(self, "提示", "请先选择一本书")

    def qqPicCopied(self):
        CtrlAltZ()

    def toWeChatByFile(self):
        if self.booksView.lastActive:
            book = self.getCurrentBook()
            copyFile(book.file_path)
            QMessageBox.about(self, "提示", "文件已复制到剪贴板")
            CtrlAltW()

    def toWeChatByPic(self):
        if self.booksView.lastActive:
            book = self.getCurrentBook()
            dig = shareByPicDialog(book, self)
            dig.copySignal.connect(self.wechatPicCopied)
            dig.show()

    def wechatPicCopied(self):
        CtrlAltW()

    def giveusStar(self):
        QDesktopServices.openUrl(QUrl('https://github.com/ruanAGroup/E-bookLibrary'))

    def setSetting(self):
        dig = SettingDialog(self)
        dig.setInitial(self.setting)
        dig.finishSignal.connect(self.onReset)
        dig.show()

    def onReset(self, toolbarSize, treeSize, bookInfoSize, searchAttr, searchMode):
        if toolbarSize:
            self.setting['toolbarSize'] = toolbarSize
        if treeSize:
            self.setting['treeSize'] = treeSize
        if bookInfoSize:
            self.setting['bookInfoSize'] = bookInfoSize
        if searchAttr:
            self.setting['searchAttr'] = searchAttr
        if searchMode:
            self.setting['searchMode'] = searchMode
        self.setSearch()
        self.toolbar.setTSize(self.setting['toolbarSize'])
        self.treeView.setTSize(self.setting['treeSize'])
        self.infoView.setTSize(self.setting['bookInfoSize'])
        book = self.getCurrentBook()
        if not book:
            book = Book()
        self.infoView.updateView(book)
        storeSetting(self.setting, self.setting_filename)

    def setSearch(self):
        self.searchLine.changeAttr(self.setting['searchAttr'])
        self.searchLine.changeAttrMode(self.setting['searchMode'])
