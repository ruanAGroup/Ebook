import time
from PyQt5.QtGui import QIntValidator, QFont
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDate, pyqtSignal, QStringListModel, QSize
from basic import strListToString
from classes import Book
from mydatabase import MyDb
from mythreads import convertThread
from fileMethods import *


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


class SettingDialog(QDialog):
    finishSignal = pyqtSignal()

    def __init__(self, parent=None):
        super(SettingDialog, self).__init__(parent)


class HighSearchDialog(QDialog):
    finishSignal = pyqtSignal()

    def __init__(self, parent=None):
        super(HighSearchDialog, self).__init__(parent)
        
        
class Setting(QWidget):
    finishSignal = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()

        self.toolbarLabel = QLabel('工具栏图标大小：')
        self.toolbarComboBox = QComboBox(self)
        self.toolbarComboBox.move(100, 20)
        self.toolbarComboBox.addItem('大')
        self.toolbarComboBox.addItem('中')
        self.toolbarComboBox.addItem('小')
        self.toolbar_size = self.toolbarComboBox.currentText()
        self.toolbarComboBox.currentTextChanged.connect(self.changetoolbar)
        self.ok_Btn1 = QPushButton("确定修改")
        self.ok_Btn1.clicked.connect(self.onOKClicked)

        self.navigationLabel = QLabel('导航页图标大小：')
        self.navigationComboBox = QComboBox(self)
        self.navigationComboBox.move(100, 20)
        self.navigationComboBox.addItem('大')
        self.navigationComboBox.addItem('中')
        self.navigationComboBox.addItem('小')
        self.navigation_size = self.navigationComboBox.currentText()
        self.navigationComboBox.currentTextChanged.connect(self.changenavigation)

        self.book_infoLabel = QLabel('书籍详情字体大小：')
        self.book_infoComboBox = QComboBox(self)
        self.book_infoComboBox.move(100, 20)
        self.book_infoComboBox.addItem('大')
        self.book_infoComboBox.addItem('中')
        self.book_infoComboBox.addItem('小')
        self.book_info_size = self.book_infoComboBox.currentText()
        self.book_infoComboBox.currentTextChanged.connect(self.changebook_info)

        self.searchModelLabel = QLabel('默认搜索条件：')
        layout = QHBoxLayout()
        self.RB1_1 = QRadioButton('按书名')
        self.RB1_1.setChecked(True)  # 默认选中RB1_1
        self.RB1_1.toggled.connect(lambda: self.btnstate(self.RB1_1))
        layout.addWidget(self.RB1_1)
        self.RB1_2 = QRadioButton('按作者')
        self.RB1_2.toggled.connect(lambda: self.btnstate(self.RB1_2))
        layout.addWidget(self.RB1_2)
        self.RB1_3 = QRadioButton('按书单')
        self.RB1_3.toggled.connect(lambda: self.btnstate(self.RB1_3))
        layout.addWidget(self.RB1_3)
        self.RB1_4 = QRadioButton('按标签')
        self.RB1_4.toggled.connect(lambda: self.btnstate(self.RB1_4))
        layout.addWidget(self.RB1_4)
        self.RB1_5 = QRadioButton('按出版社')
        self.RB1_5.toggled.connect(lambda: self.btnstate(self.RB1_5))
        layout.addWidget(self.RB1_3)
        self.RB1_6 = QRadioButton('按ISBN')
        self.RB1_6.toggled.connect(lambda: self.btnstate(self.RB1_6))
        layout.addWidget(self.RB1_6)

        self.searchModelLabel = QLabel('默认匹配模式：')
        layout = QHBoxLayout()
        self.RB2_1 = QRadioButton('正则匹配')
        self.RB2_1.setChecked(True)  # 默认选中RB1_1
        self.RB2_1.toggled.connect(lambda: self.btnstate1(self.RB2_1))
        layout.addWidget(self.RB2_1)
        self.RB2_2 = QRadioButton('准确匹配')
        self.RB2_2.toggled.connect(lambda: self.btnstate1(self.RB2_2))
        layout.addWidget(self.RB2_2)
        self.RB2_3 = QRadioButton('模糊匹配')
        self.RB2_3.toggled.connect(lambda: self.btnstate1(self.RB2_3))
        layout.addWidget(self.RB2_3)
        layout.addWidget(self.ok_Btn1)
        self.setLayout(layout)

    def onOKClicked(self):
        sortMode = "按作者"
        searchMode = "模糊匹配"
        self.finishSignal.emit(sortMode, searchMode)
        self.close()

    def changetoolbar(self, attr):
        self.toolbar_size = attr
        model = QStringListModel()
        if attr == '大':
            model.MyToolBar.setIconSize(QSize(200, 200))
        elif attr == '中':
            model.MyToolBar.setIconSize(QSize(100, 100))
        else:
            model.MyToolBar.setIconSize(QSize(50, 50))
        self.inputCompleter.setModel(model)

    def changenavigation(self, attr):
        self.navigation_size = attr
        model = QStringListModel()
        if attr == '大':
            model.MyTree.setIconSize(QSize(100, 100))
        elif attr == '中':
            model.MyTree.setIconSize(QSize(50, 50))
        else:
            model.MyTree.setIconSize(QSize(25, 25))
        self.inputCompleter.setModel(model)

    def changebook_info(self, attr):
        self.book_info_size = attr
        model = QStringListModel()
        if attr == '大':
            model.MyList.temwidget.setFont(QFont("", 30))
        elif attr == '中':
            model.MyList.temwidget.setFont(QFont("", 14))
        else:
            model.MyList.temwidget.setFont(QFont("", 7))
        self.inputCompleter.setModel(model)

    def btnstate(self, btn):
        self.searchAttr = self.btn.text()
        self.searchBy.currentTextChanged.connect(self.changeAttr)
        if btn.text() == "按书名":
            if btn.isChecked():
                self.searchBy.setCurrentIndex(0)
        elif btn.text() == "按作者":
            if btn.isChecked():
                self.searchBy.setCurrentIndex(1)
        elif btn.text() == "按书单":
            if btn.isChecked():
                self.searchBy.setCurrentIndex(2)
        elif btn.text() == "按标签":
            if btn.isChecked():
                self.searchBy.setCurrentIndex(3)
        elif btn.text() == "按出版社":
            if btn.isChecked():
                self.searchBy.setCurrentIndex(4)
        else:  # 按ISBN
            if btn.isChecked():
                self.searchBy.setCurrentIndex(5)

    def btnstate1(self, btn):
        if btn.text() == '正则匹配':
            if btn.isChecked():
                self.searchMode.setCurrentIndex(2)
        elif btn.text() == "准确匹配":
            if btn.isChecked():
                self.searchMode.setCurrentIndex(0)
        else:  # 模糊匹配
            if btn.isChecked():
                self.searchMode.setCurrentIndex(1)
