# 主程序
from ui import BookManager
from PyQt5.QtWidgets import QApplication
import sys
import os
from settings import readSetting, storeSetting


setting_file_name = 'setting.json'
if not os.path.exists(setting_file_name):
    initialSetting = {
        "toolbarSize": "大",
        "treeSize": "大",
        "bookInfoSize": "大",
        "searchAttr": "按书名",
        "searchMode": "准确匹配",
    }
    storeSetting(initialSetting, setting_file_name)
setting = readSetting(setting_file_name)
app = QApplication(sys.argv)
bookManager = BookManager(setting, setting_file_name)
sys.exit(app.exec_())


