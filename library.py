# 1、需要安装mysql数据库才能启动此代码
# 2、要连接自己数据库，就需要自己修改下面的ip、用户名、密码、database等
# 3、存储书籍的数据库需要按代码中建立，如果已经建好，就需要对应改下代码中的字段名

import pymysql

# 数据库连接类
class DbConn(object):

    def __init__(self):
        host = "172.31.50.219"
        user = "root"
        password = "antiy666"
        database = "test"
        self.__conn = pymysql.connect(
                host=host,
                user=user, password=password,
                database=database,
                charset="utf8")
        self.__cursor = self.__conn.cursor()
    
    def save_data(self, data):
        """ 数据保存 """
        sql ="insert into bookinfo (title,author,isbn,category) values (%s,%s,%s,%s);"
        self.__cursor.execute(sql, data)
        self.__conn.commit()
        
    def query_data(self, query_type, query_data):
        """ 数据查询 """
        sql = f"select * from bookinfo where {query_type}='{query_data}'"
        self.__cursor.execute(sql)
        return self.__cursor.fetchall()

    def close(self):
        """ 断开连接 """
        self.__cursor.close()
        self.__conn.close()


# 书籍操作类
class LibraryBook(object):

    def __init__(self):
        self.__db  = DbConn()
        self.input_handle()
    
    def input_handle(self):
        """ 用户输入处理 """
        self.__type_num = input("请选择要执行的功能：\n 1、添加书籍\n 2、查询数据\n 3、退出\n请选择功能(1/2/3)：")
        if self.__type_num == "1":
            self.add_book()
        elif self.__type_num == "2":
            self.query_book()
        else:
            self.quit()
    
    def add_book(self):
        """ 添加书籍 """
        print("您选择了添加书籍功能!")
        title  = input("请输入书籍的标题：")
        author = input("请输入书籍的作者：")
        isbn_num = input("请输入书籍的ISBN号：")
        category = input("请输入书籍的分类：")
        print(title, author, isbn_num, category)
        data = [title, author, isbn_num, category]
        self.__db.save_data(data)
        print("书籍添加成功！\n")
        input("按任意键继续！")
        self.input_handle()

    def query_book(self):
        """ 查询书籍 """
        query_type = input("请输入查询条件 1、标题 2、作者 3、ISBN号 4、分类 5、退出\n请输入序号(1/2/3/4/5):")
        query_translate = {"1": "title", "2": "author", "3": "isbn", "4": "category"}
        if query_type == "5":
            self.quit()
        query_type = query_translate.get(query_type, "")
        if not query_type:
            print("请输入正确的数字！")
            self.query_book()
        query_data = input("请输入要查询的内容：")
        result = self.__db.query_data(query_type, query_data)
        print("\n查询结果如下:")
        for data in result:
            print(data[0], data[1], data[2], data[3])
        input("\n按任意键继续！")
        self.input_handle()
    
    def quit(self):
        """ 退出 """
        print("退出成功，欢迎下次光临！")
        self.__db.close()


if __name__ == "__main__":
    lib = LibraryBook()