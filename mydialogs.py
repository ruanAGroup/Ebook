import time

from PyQt5 import QtGui
from PyQt5.QtGui import QIntValidator, QFont, QPixmap
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDate, pyqtSignal, QStringListModel, QSize, Qt
from basic import strListToString, setClipPic, CtrlAltZ
from classes import Book
from mydatabase import MyDb
from mythreads import convertThread
from fileMethods import *
from share import getCover


class MyComboBox(QComboBox):
    def __init__(self, parent=None):
        super(MyComboBox, self).__init__(parent)
        self.standModel = QtGui.QStandardItemModel(self)
        self.setModel(self.standModel)
        self.view().pressed.connect(self.onItemClicked)

    def onItemClicked(self, index):
        item = self.model().itemFromIndex(index)
        if item.checkState() == Qt.Checked:
            item.setCheckState(Qt.Unchecked)
        else:
            item.setCheckState(Qt.Checked)

    def getAllCheckedItems(self):
        items = []
        for index in range(self.count()):
            item = self.model().item(index)
            if item.checkState() == Qt.Checked:
                items.append(int(item.text().split('-')[-1]))
        return items


class EditDataDialog(QDialog):
    changeSignal = pyqtSignal(int)

    def __init__(self, db: MyDb, book: Book, parent=None):
        super(EditDataDialog, self).__init__(parent)
        self.db = db
        self.book = book
        self.form = QFormLayout()
        self.nameLabel = QLabel("书名")
        self.nameInput = QLineEdit()
        if book.name:
            self.nameInput.setText(book.name)
        self.authorLabel = QLabel("作者")
        self.authorInput = QLineEdit()
        if book.authors:
            self.authorInput.setText(strListToString(book.authors))
        self.pub_dateLabel = QLabel("出版日期")
        self.pub_dateInput = QDateEdit()
        if book.pub_date:
            date = QDate()
            self.pub_dateInput.setDate(date.fromString(book.pub_date, 'yyyyMMdd'))
        self.publisherLabel = QLabel("出版社")
        self.publisherInput = QLineEdit()
        if book.publisher:
            self.publisherInput.setText(book.publisher)
        self.isbnLabel = QLabel("ISBN")
        self.isbnInput = QLineEdit()
        if book.isbn:
            self.isbnInput.setText(book.isbn)
        self.languageLabel = QLabel("语言")
        self.languageInput = QLineEdit()
        if book.language:
            self.languageInput.setText(book.language)
        self.ratingLabel = QLabel("评分")
        self.ratingInput = QLineEdit()
        self.ratingInput.setValidator(QIntValidator(0, 5))
        if book.rating:
            self.ratingInput.setText(str(book.rating))
        self.tagsLabel = QLabel("标签")
        self.tagsInput = QLineEdit()
        if book.tags:
            self.tagsInput.setText(strListToString(book.tags))
        self.booklistLabel = QLabel("书单")
        self.booklistInput = QLineEdit()
        if book.bookLists:
            self.booklistInput.setText(strListToString(book.bookLists))
        self.okButton = QPushButton("保存并退出")
        self.cancleButton = QPushButton("不保存退出")
        self.form.addRow(self.nameLabel, self.nameInput)
        self.form.addRow(self.authorLabel, self.authorInput)
        self.form.addRow(self.pub_dateLabel, self.pub_dateInput)
        self.form.addRow(self.publisherLabel, self.publisherInput)
        self.form.addRow(self.isbnLabel, self.isbnInput)
        self.form.addRow(self.languageLabel, self.languageInput)
        self.form.addRow(self.ratingLabel, self.ratingInput)
        self.form.addRow(self.tagsLabel, self.tagsInput)
        self.form.addRow(self.booklistLabel, self.booklistInput)
        self.form.addRow(self.okButton, self.cancleButton)
        self.setLayout(self.form)
        self.okButton.clicked.connect(self.onOK)
        self.cancleButton.clicked.connect(self.onCancle)

    def onOK(self):
        self.book.name = self.nameInput.text()
        self.book.setAuthors(self.db, parseStrListString(self.authorInput.text()))
        self.book.pub_date = self.pub_dateInput.date().toString('yyyyMMdd')
        self.book.publisher = self.publisherInput.text()
        self.book.isbn = self.isbnInput.text()
        self.book.language = self.languageInput.text()
        if self.ratingInput.text():
            self.book.rating = int(self.ratingInput.text())
        else:
            self.book.rating = 0
        self.book.tags = parseStrListString(self.tagsInput.text())
        self.book.setBookLists(self.db, parseStrListString(self.booklistInput.text()))
        self.book.setMetadata()
        self.book.updateDB(self.db)
        self.changeSignal.emit(self.book.ID)
        self.close()

    def onCancle(self):
        self.close()


class ImportFileEditDialog(QDialog):
    changeSignal = pyqtSignal(str, list, str, int)

    def __init__(self, name=None, parent=None):
        super(ImportFileEditDialog, self).__init__(parent)
        self.nameLabel = QLabel("书名")
        self.nameInput = QLineEdit()
        if name:
            self.nameInput.setText(name)
        self.authorLabel = QLabel("作者")
        self.authorInput = QLineEdit()
        self.languageLabel = QLabel("语言")
        self.languageInput = QLineEdit()
        self.ratingLabel = QLabel("评分")
        self.ratingInput = QLineEdit()
        self.ratingInput.setValidator(QIntValidator(0, 5))
        self.okBtn = QPushButton("确定")
        self.okBtn.clicked.connect(self.onClicked)
        self.cancleBtn = QPushButton("取消转换")
        self.cancleBtn.clicked.connect(self.onCancle)
        self.form = QFormLayout()
        self.form.addRow(self.nameLabel, self.nameInput)
        self.form.addRow(self.authorLabel, self.authorInput)
        self.form.addRow(self.languageLabel, self.languageInput)
        self.form.addRow(self.ratingLabel, self.ratingInput)
        self.form.addRow(self.okBtn, self.cancleBtn)
        self.setLayout(self.form)

    def onClicked(self):
        name = self.nameInput.text()
        authors = parseStrListString(self.authorInput.text())
        language = self.languageInput.text()
        if self.ratingInput.text():
            rating = int(self.ratingInput.text())
        else:
            rating = 0
        self.changeSignal.emit(name, authors, language, rating)
        self.close()

    def onCancle(self):
        self.close()


class ImportFileDialog(QDialog):
    finishSignal = pyqtSignal(str, str, list, str, int)

    def __init__(self, basepath, db, parent=None):
        super(ImportFileDialog, self).__init__(parent)
        self.basePath = basepath
        self.db = db
        self.filepath, _ = QFileDialog.getOpenFileName(self, "选择文件", ".", "docx or markdown file(*.docx *.md)")
        if self.filepath:
            direcPath, file = os.path.split(self.filepath)
            self.filename, self.filesufix = file.split('.')
            dig = ImportFileEditDialog(self.filename, self)
            dig.changeSignal.connect(self.onConvert)
            dig.show()

    def onConvert(self, name, authors, language, rating):
        if not name:
            name = self.filename
        bookPath, bookFilePath = getFilePath(self.basePath, name, self.db.getID(), self.filepath)
        if not bookPath:
            return
        pdfFilePath = os.path.join(bookPath, name+'.pdf')
        if self.filesufix == 'md':
            t = convertThread(mdToPdf, (bookFilePath, pdfFilePath))
        else:  # docx
            t = convertThread(docxToPdf, (bookFilePath, pdfFilePath))
        t.finishSignal.connect(lambda: self.finishConvert(pdfFilePath, name, authors, language, rating))
        t.start()
        time.sleep(1)

    def finishConvert(self, pdfFilePath, name, authors, language, rating):
        self.finishSignal.emit(pdfFilePath, name, authors, language, rating)


class ExportINFODialog(QDialog):
    finishSignal = pyqtSignal(str)

    def __init__(self, db: MyDb, parent=None):
        super(ExportINFODialog, self).__init__(parent)
        self.db = db
        file_name, _ = QFileDialog.getSaveFileName(self, "保存文件", ".", "csv file(*.csv)")
        if file_name:
            rows = self.db.getAllBookRows()
            headers = ['书名', '作者', '出版日期', '出版社', 'ISBN', '语言', '文件路径', '封面路径', '评分', '标签', '书单']
            t = convertThread(toCSV, (file_name, headers, rows))
            t.finishSignal.connect(lambda: self.FinishExport(file_name))
            t.start()
            time.sleep(1)

    def FinishExport(self, filename):
        self.finishSignal.emit(filename)
        

class HighSearchDialog(QDialog):
    finishSignal = pyqtSignal(str, list, str, list)

    def __init__(self, parent=None):
        super(HighSearchDialog, self).__init__(parent)
        
        self.booknameLabel = QLabel("书名:")
        self.booknameInput = QLineEdit()
        self.bookauthorLabel = QLabel("作者:")
        self.bookauthorInput = QLineEdit()
        self.pressLabel = QLabel("出版社：")
        self.pressInput = QLineEdit()
        self.booktagLabel = QLabel("标签：")
        self.booktagInput = QLineEdit()

        self.okBtn = QPushButton("确定搜索")
        self.okBtn.clicked.connect(self.onClicked)
        self.cancleBtn = QPushButton("取消搜索")
        self.cancleBtn.clicked.connect(self.onCancle)

        self.form = QFormLayout()
        self.form.addRow(self.booknameLabel, self.booknameInput)
        self.form.addRow(self.bookauthorLabel, self.bookauthorInput)
        self.form.addRow(self.pressLabel, self.pressInput)
        self.form.addRow(self.booktagLabel, self.booktagInput)
        self.form.addRow(self.okBtn, self.cancleBtn)
        self.setLayout(self.form)

    def onClicked(self):
        if self.booknameInput.text():
            name = self.booknameInput.text()
        else:
            name = ""
        if self.bookauthorInput.text():
            authors = parseStrListString(self.bookauthorInput.text())
        else:
            authors = []
        if self.pressInput.text():
            press = self.pressInput.text()
        else:
            press = ""
        if self.booktagInput.text():
            booktag = parseStrListString(self.booktagInput.text())
        else:
            booktag = []
        self.finishSignal.emit(name, authors, press, booktag)
        self.close()

    def onCancle(self):
        self.close()
        
        
class SettingDialog(QDialog):
    finishSignal = pyqtSignal(str, str, str, str, str)

    def __init__(self, parent=None):
        super(SettingDialog, self).__init__(parent)

        self.toolbarLabel = QLabel('工具栏图标大小：')
        self.toolbarComboBox = QComboBox(self)
        self.toolbarComboBox.move(100, 20)
        self.toolbarComboBox.addItem('大')
        self.toolbarComboBox.addItem('中')
        self.toolbarComboBox.addItem('小')

        self.navigationLabel = QLabel('导航页图标大小：')
        self.navigationComboBox = QComboBox(self)
        self.navigationComboBox.move(100, 20)
        self.navigationComboBox.addItem('大')
        self.navigationComboBox.addItem('中')
        self.navigationComboBox.addItem('小')

        self.book_infoLabel = QLabel('书籍详情字体大小：')
        self.book_infoComboBox = QComboBox(self)
        self.book_infoComboBox.move(100, 20)
        self.book_infoComboBox.addItem('大')
        self.book_infoComboBox.addItem('中')
        self.book_infoComboBox.addItem('小')

        self.searchLabel = QLabel('默认搜索条件：')
        self.searchComboBox = QComboBox(self)
        self.searchComboBox.move(100, 20)
        self.searchComboBox.addItem('按书名')
        self.searchComboBox.addItem('按作者')
        self.searchComboBox.addItem('按书单')
        self.searchComboBox.addItem('按标签')
        self.searchComboBox.addItem('按出版社')
        self.searchComboBox.addItem('按ISBN')

        self.searchModeLabel = QLabel('默认匹配模式：')
        self.searchModeComboBox = QComboBox(self)
        self.searchModeComboBox.move(100, 20)
        self.searchModeComboBox.addItem('准确匹配')
        self.searchModeComboBox.addItem('模糊匹配')
        self.searchModeComboBox.addItem('正则匹配')

        self.ok_Btn1 = QPushButton("确定修改")
        self.ok_Btn1.clicked.connect(self.onOK_Clicked)

        self.cancle_Btn1 = QPushButton("取消修改")
        self.cancle_Btn1.clicked.connect(self.cancle_Clicked)

        self.form = QFormLayout()
        self.form.addRow(self.toolbarLabel, self.toolbarComboBox)
        self.form.addRow(self.navigationLabel, self.navigationComboBox)
        self.form.addRow(self.book_infoLabel, self.book_infoComboBox)
        self.form.addRow(self.searchLabel, self.searchComboBox)
        self.form.addRow(self.searchModeLabel, self.searchModeComboBox)
        self.form.addRow(self.ok_Btn1, self.cancle_Btn1)
        self.setLayout(self.form)

    def onOK_Clicked(self):
        toolbarsize = self.toolbarComboBox.currentText()   # 工具栏图标大小
        navigationsize = self.navigationComboBox.currentText()  # 导航条图标大小
        bookinfosize = self.book_infoComboBox.currentText()   # 书籍详情字体大小
        searchby = self.searchComboBox.currentText()  # 搜索条件 例如：“按作者”
        searchmode = self.searchModeComboBox.currentText()  # 匹配模式 例如“正则匹配”
        self.finishSignal.emit(toolbarsize, navigationsize, bookinfosize, searchby, searchmode)
        self.close()

    def cancle_Clicked(self):
        self.close()

    def setInitial(self, setting):
        self.toolbarComboBox.setCurrentText(setting['toolbarSize'])
        self.navigationComboBox.setCurrentText(setting['treeSize'])
        self.book_infoComboBox.setCurrentText(setting['bookInfoSize'])
        self.searchComboBox.setCurrentText(setting['searchAttr'])
        self.searchModeComboBox.setCurrentText(setting['searchMode'])


class CreateBookListDialog(QDialog):
    finishSignal = pyqtSignal(str, list)

    def __init__(self, parent=None):
        super(CreateBookListDialog, self).__init__(parent)
        self.form = QFormLayout()
        self.label1 = QLabel("书单名")
        self.input1 = QLineEdit()
        self.label2 = QLabel("添加书籍")
        self.input2 = MyComboBox()
        self.okBtn = QPushButton("确定")
        self.okBtn.clicked.connect(self.onOk)
        self.cancleBtn = QPushButton("取消")
        self.cancleBtn.clicked.connect(self.onCancle)
        self.form.addRow(self.label1, self.input1)
        self.form.addRow(self.label2, self.input2)
        self.form.addRow(self.okBtn, self.cancleBtn)
        self.setLayout(self.form)

    def onOk(self):
        booklist_name = self.input1.text()
        book_ids = self.input2.getAllCheckedItems()
        self.finishSignal.emit(booklist_name, book_ids)
        self.close()

    def onCancle(self):
        self.close()


class changeCoverDialog(QDialog):
    coverChangeSignal = pyqtSignal(QPixmap)

    def __init__(self, book, parent=None):
        super(changeCoverDialog, self).__init__(parent)
        self.book = book
        self.coverLabel = QLabel()
        self.coverLabel.setPixmap(QPixmap(book.cover_path).scaled(365, 458))
        self.choseFileBtn = QPushButton("选择图片")
        self.generateCoverBtn = QPushButton("生成封面")
        self.okBtn = QPushButton("确定")
        self.cancleBtn = QPushButton("取消")
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        hbox.addWidget(self.okBtn)
        hbox.addWidget(self.cancleBtn)
        vbox.addWidget(self.coverLabel)
        vbox.addWidget(self.choseFileBtn)
        vbox.addWidget(self.generateCoverBtn)
        tempWidget = QWidget()
        tempWidget.setLayout(hbox)
        vbox.addWidget(tempWidget)
        self.setLayout(vbox)
        self.choseFileBtn.clicked.connect(self.onChoseFile)
        self.generateCoverBtn.clicked.connect(self.onGenerateCover)
        self.okBtn.clicked.connect(self.onOK)
        self.cancleBtn.clicked.connect(self.onCancle)

    def onChoseFile(self):
        filename, _ = QFileDialog.getOpenFileName(self, "选择封面图片", ".", "image files(*.png *.jpg *.jpeg *.bmp)")
        if filename:
            self.coverLabel.setPixmap(QPixmap(filename).scaled(365, 458))

    def onGenerateCover(self):
        img = getCover(self.book)
        self.coverLabel.setPixmap(QPixmap().fromImage(img).scaled(365, 458))

    def onOK(self):
        pic = self.coverLabel.pixmap()
        self.coverChangeSignal.emit(pic)
        self.close()

    def onCancle(self):
        self.close()
