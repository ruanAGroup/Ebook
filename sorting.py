def  sortByName(books):
    for i in range(len(books.name)):

        for j in range(i):

            if books.name[i] < books.name[j]:
                books.insert(j, books.pop(i))
                break

    return   books


def sortByDate(books):
    length = len(books)
    while length > 0:
        for i in range(length - 1):
            if books.date[i] > books.date[i + 1]:
               books(length+1)=books(i)
                books(i)=books(i+1)
                books(i+1)=books[length+1]
        length -= 1
     return books

def sortByAuthor(books):
    if len(books) <= 1:
        return books
    num = int(len(books)/2)
    left = sortByAuthor(books[:num]) #将列表从中间分为两部分
    right = sortByAuthor(books[num:])
    return Merge(left, right) #合并两个列表

def Merge(left,right):
    r, l=0, 0
    result=[]
    while l<len(left) and r<len(right):
        if left.author[l] < right.author[r]:
            result.append(left[l])
            l += 1
        else:
            result.append(right[r])
            r += 1
    result += left[l:]
    result += right[r:]
    return result

def sortByPubulisher(books)
   length=len(books)
   for i in range(len(books))
       for j in range(len(books)-i)
           if books.publisher[i]> books.publisher[i+1]
               books[length+1]= books[i]
               books[i]= books[i+1]
               books[i+1]= books[length+1]
    return books

