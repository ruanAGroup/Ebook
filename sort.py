# 此文件存储排序、分类相关算法

def sortByName(books):
    num = len(books)
    for i in range(num):
        curname = books[i].name
        curnum = i
        for j in range(i+1, num):
            if books[j].name > curname:
                curname = books[j].num
                curnum = j
        if i != curnum:
            temp = books[i]
            books[i] = books[curnum]
            books[curnum] = temp
    return books

