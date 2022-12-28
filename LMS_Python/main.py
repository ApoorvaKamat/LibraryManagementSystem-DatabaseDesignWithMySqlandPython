import mysql.connector as sqlConn
from tkinter import *
from ttkthemes import ThemedTk
from lmsAppGui import *

# Modify the Mysql connection details below to connct to your database

libraryDatabase = sqlConn.connect(
    host="localhost",
    username="root",
    password="EnterYourPasswordHere",
    database="bookstore"
) 
cursor = None
if __name__ == '__main__':
    root = ThemedTk(theme="Adapta")
    tool = LmsAppGui(root)
    root.mainloop()