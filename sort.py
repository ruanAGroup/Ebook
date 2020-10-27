# 此文件存储排序、分类相关算法
#为了方便查看排序结果，将排序结果转换存储为xlsx类型文件（可删除），排序结果结构为DataFrame表格型的books_info
import pandas as pd
def Merge_sort(ls):
    #合并左右子序列函数
    def merge(arr, left, mid, right):
        temp = []     # 中间数组
        i = left      # 左段子序列起始
        j = mid + 1   # 右段子序列起始
        while i <= mid and j <= right:
            if arr[i] <= arr[j]:
                temp.append(arr[i])
                i += 1
            else:
                temp.append(arr[j])
                j += 1
        while i <= mid:
            temp.append(arr[i])
            i += 1
        while j <= right:
            temp.append(arr[j])
            j += 1
        for i in range(left, right+1):     
            arr[i] = temp[i-left]
    #递归调用归并排序
    def mSort(arr, left, right):
        if left >= right:
            return
        mid = (left + right) // 2
        mSort(arr, left, mid)
        mSort(arr, mid+1, right)
        merge(arr, left, mid, right)
 
    n = len(ls)
    if n <= 1:
        return ls
    mSort(ls, 0, n-1)
    return ls

def pd_sort(books_info, by):
    # books_info_dct = {}
    key_list, value_list, index_list = [], [], []
    for i in range(len(books_info)):
        key_list.append(books_info[by][i]) # 选取by列i行的元素作为key
        value_list.append(books_info.loc[[i]]) # 选取第i行作为value
        # books_info_dct[books_info[by][i+1]] = books_info.loc[[i+1]] # 选取by列i行的元素作为字典的key,第i行作为字典的value
    key_list_dct = {}
    key_list = [str(k) for k in key_list] 
    for i in range(len(key_list)):
        if not key_list_dct.get(key_list[i]): # 若未出现过该key,则创建空列表
            key_list_dct[key_list[i]] = []
        key_list_dct[key_list[i]].append(i) # 选取by列i行的元素作为字典的key,i作为字典的value
    key_list = Merge_sort(key_list) # 对key_list归并排序
    # print(key_list_dct)
    for key in key_list: # 通过key_list_dct,从排序后的key_list中得到index_list
        index_list.append(key_list_dct[key][0]) # 取第一个
        del key_list_dct[key][0] # 删除第一个
    res_list = [value_list[index] for index in index_list] # 从index_list中得到结果列表res_list
    res_books_info = res_list[0] # 结果数据框
    res_books_info = res_books_info.append(res_list[1:])
    # for i in range(1, len(books_info)):
    #     res_books_info.append(res_list[i])
    return res_books_info

# 按照书名排序
def sortByName(books_info):
    by = 'Book-name'
    books_info = pd_sort(books_info, by)
    file_name = 'sortByName'
    books_info.to_csv('./data/csv/' + file_name + '.csv', index=True, header=True)
    csv_to_xlsx_pd(file_name)
    
# 按照出版日期排序
def sortByDate(books_info):
    by = 'Publish-time'
    books_info = pd_sort(books_info, by)
    # books_info.sort_values(by=['Publish-time'], ascending=True, inplace=True)
    file_name = 'sortByDate'
    books_info.to_csv('./data/csv/' + file_name + '.csv', index=True, header=True)
    csv_to_xlsx_pd(file_name)

# 按照作者排序
def sortByAuthor(books_info):
    by = 'Author'
    books_info = pd_sort(books_info, by)
    # books_info.sort_values(by=['Author'], ascending=True, inplace=True)
    file_name = 'sortByAuthor'
    books_info.to_csv('./data/csv/' + file_name + '.csv', index=True, header=True)
    csv_to_xlsx_pd(file_name)

# 按照出版商排序
def sortByPublisher(books_info):
    by = 'Publisher'
    books_info = pd_sort(books_info, by)
    # books_info.sort_values(by=['Publisher'], ascending=True, inplace=True)
    file_name = 'sortByPublisher'
    books_info.to_csv('./data/csv/' + file_name + '.csv', index=True, header=True)
    csv_to_xlsx_pd(file_name)

# 计算匹配度, 计算keyword和wordList里每一个单词之间的匹配度，并将匹配度数组返回
def calcu_match(keyword, wordList):
    pass

# 根据匹配度排序
def sortBtMatch(match_list):
    pass

def csv_to_xlsx_pd(file_name):
    csv = pd.read_csv('./data/csv/' + file_name  + '.csv', encoding='utf-8')
    csv.to_excel('./data/xlsx/' + file_name + '.xlsx', sheet_name=file_name)

def main():
    books_info = pd.read_csv('./data/csv/novel_books_info.csv', low_memory=False) # 读取书籍信息
    sortByName(books_info) # 按照书名排序
    sortByDate(books_info) # 按照出版日期排序
    sortByAuthor(books_info) # 按照作者排序
    sortByPublisher(books_info) # 按照出版商排序
    # res_calcu_match = calcu_match(keyword, wordList) # 计算匹配度, 计算keyword和wordList里每一个单词之间的匹配度，并将匹配度数组返回
    # sortBtMatch(match_list) # 根据匹配度排序


if __name__ == '__main__':
    main()


