# 此文件存储用户的设置，以及一些重要的参数
# 需要将这些信息存储到一个文件中
# 每次打开应用时需要从文件中读取相应的参数
# 目前计划使用json文件存储
import json


def storeSetting(dictionary, filename):
    try:
        with open(filename, 'w') as f_obj:
            json.dump(dictionary, f_obj)
    except FileNotFoundError:
        return None


def readSetting(filename):
    try:
        with open(filename) as f_obj:
            dictionary = json.load(f_obj)
    except FileNotFoundError:
        return None
    else:
        return dictionary

