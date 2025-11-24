import pymysql

dataBase = pymysql.connect(
    host='localhost',
    user='root',
    password='123456789'
)

cursorObject = dataBase.cursor()
cursorObject.execute("CREATE DATABASE djyl")
print("All Done!")
