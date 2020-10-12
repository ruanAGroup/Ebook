import sys
import os
import editor
import txetedit
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QApplication, QColorDialog, QFontDialog, QTextEdit, QFileDialog, QMessageBox
from PyQt5.QtCore import QFile, QFileInfo
from PyQt5.QtGui import QPalette, QTextCursor


class Editor(QtWidgets.QMainWindow, editor.Ui_MainWindow):
    def __init__(self, parent=None):
        super(Editor, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Notepad")
        self.actionOpen.triggered.connect(self.fileOpen)
        self.actionNew.triggered.connect(self.fileNew)
        self.actionSave.triggered.connect(self.fileSave)
        self.actionClose.triggered.connect(self.closeEvent)
        self.actionPile.triggered.connect(self.filePile)
        self.actionHorizontal.triggered.connect(self.fileHorizontal)
        self.actionVertical.triggered.connect(self.fileVertical)
        self.actionDelete.triggered.connect(self.fileUndo)
        self.actionRecover.triggered.connect(self.fileRedo)
        self.actionCopy.triggered.connect(self.fileCopy)
        self.actionCut.triggered.connect(self.fileCut)
        self.actionPaste.triggered.connect(self.filePaste)
        self.actionBold.triggered.connect(self.fileBold)
        self.actionItalic.triggered.connect(self.fileItalic)
        self.actionUnderline.triggered.connect(self.fileUnderline)
        self.fontComboBox.currentFontChanged.connect(self.fileChangeFont)
        self.actionSearch.triggered.connect(self.fileSearch)
        self.actionLeft.triggered.connect(self.fileLeft)
        self.actionRight.triggered.connect(self.fileRight)
        self.actionFont.triggered.connect(self.fileFontBox)
        self.actionColor.triggered.connect(self.fileColorBox)

    def fileFontBox(self):
        font, okPressed = QFontDialog.getFont()
        if okPressed:
            self.mdiArea.activeSubWindow().widget().setCurrentFont(font)

    def fileColorBox(self):
        col = QColorDialog.getColor()
        if col.isValid():
            self.mdiArea.activeSubWindow().widget().setTextColor(col)

    def fileLeft(self):
        self.mdiArea.activeSubWindow().widget().setAlignment(Qt.AlignLeft)

    def fileRight(self):
        self.mdiArea.activeSubWindow().widget().setAlignment(Qt.AlignRight)

    def fileCenter(self):
        self.mdiArea.activeSubWindow().widget().setAlignment(Qt.AlignCenter)

    def fileHorizontal(self):
        wList = self.mdiArea.subWindowList()
        size = len(wList)
        if size > 0:
            position = QtCore.QPoint(0, 0)
            for w in wList:
                rect = QtCore.QRect(0, 0, self.mdiArea.width() / size,
                                    self.mdiArea.height())
                w.setGeometry(rect)
                w.move(position)
                position.setX(position.x() + w.width())

    def fileVertical(self):
        wList = self.mdiArea.subWindowList()
        size = len(wList)
        if size > 0:
            position = QtCore.QPoint(0, 0)
            for w in wList:
                rect = QtCore.QRect(0, 0, self.mdiArea.width(),
                                    self.mdiArea.height() / size)
                w.setGeometry(rect)
                w.move(position)
                position.setY(position.y() + w.height())

    def fileChangeFont(self, font):
        self.mdiArea.activeSubWindow().widget().setCurrentFont(font)

    def fileSearch(self):
        pattern, okPressed = QtWidgets.QInputDialog.getText(self,
                                                            "查找", "查找字符串:", QtWidgets.QLineEdit.Normal, "")
        if okPressed and pattern != '':
            sub = self.mdiArea.activeSubWindow().widget()
            sub.moveCursor(QTextCursor.StartOfLine, QTextCursor.MoveAnchor)
            if sub.find(pattern):
                palette = sub.palette()
                palette.setColor(QPalette.Highlight, palette.color(QPalette.Active, QPalette.Highlight))
                sub.setPalette(palette)

    def fileBold(self):
        sub = self.mdiArea.activeSubWindow().widget()
        tmpFormat = sub.currentCharFormat()
        if tmpFormat.fontWeight() == QtGui.QFont.Bold:
            tmpFormat.setFontWeight(QtGui.QFont.Normal)
        else:
            tmpFormat.setFontWeight(QtGui.QFont.Bold)
        sub.mergeCurrentCharFormat(tmpFormat)

    def fileItalic(self):
        tmpTextBox = self.mdiArea.activeSubWindow().widget()
        tmpTextBox.setFontItalic(not tmpTextBox.fontItalic())

    def fileUnderline(self):
        tmpTextBox = self.mdiArea.activeSubWindow().widget()
        tmpTextBox.setFontUnderline(not tmpTextBox.fontUnderline())

    def fileCopy(self):
        self.mdiArea.activeSubWindow().widget().copy()

    def fileCut(self):
        self.mdiArea.activeSubWindow().widget().cut()

    def filePaste(self):
        self.mdiArea.activeSubWindow().widget().paste()

    def fileRedo(self):
        self.mdiArea.activeSubWindow().widget().redo()

    def fileUndo(self):
        self.mdiArea.activeSubWindow().widget().undo()

    def filePile(self):
        if len(self.mdiArea.subWindowList()) > 1:
            self.mdiArea.cascadeSubWindows()

    def fileSave(self):
        tmpTextEdit = self.mdiArea.activeSubWindow()
        tmpTextEdit = tmpTextEdit.widget()
        if tmpTextEdit is None or not isinstance(tmpTextEdit, QTextEdit):
            return True
        tmpTextEdit.save()

    def fileOpen(self):
        filename, filetype = QFileDialog.getOpenFileName(self, "打开文件", "C:", "Text files (*.txt);;HTML files (*html)")
        if filename:
            for window in self.mdiArea.subWindowList():
                textEdit = window.widget()
                if textEdit.filename == filename:
                    self.mdiArea.setActiveSubWindow(window)
                    break
            else:
                self.loadFile(filename)

    def fileNew(self):
        tmpTextEdit = txetedit.TextEdit()
        self.mdiArea.addSubWindow(tmpTextEdit)
        tmpTextEdit.show()

    def loadFile(self, filename):
        tmpTextEdit = txetedit.TextEdit(filename)
        tmpTextEdit.load()
        self.mdiArea.addSubWindow(tmpTextEdit)
        tmpTextEdit.show()

    def closeEvent(self, event):
        unSaveFile = 0
        for window in self.mdiArea.subWindowList():
            textEdit = window.widget()
            if textEdit.isModified():
                unSaveFile += 1
        if unSaveFile != 0:
            dlg = QMessageBox.warning(self, "Notepad", "{0}个文档尚未保存，是否关闭？".format(unSaveFile),
                                      QMessageBox.Yes | QMessageBox.No)
            if dlg == QMessageBox.Yes:
                QtCore.QCoreApplication.quit()
            elif dlg == QMessageBox.No:
                event.ignore()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = Editor()
    ex.show()
    app.exec_()
