from tkinter import *
from tkinter import simpledialog, messagebox
from tkinter.ttk import Treeview
import mysql.connector as sqlConn

from main import libraryDatabase

class CheckInBook:
    def __init__(self, master):
        self.parent = master

        self.bookForCheckInID = None
        self.search_string = None
        self.data = None
        self.results = None

        self.searchLabel = Label(self.parent, text="Search here: Borrower ID, Borrower Name or ISBN")
        self.searchLabel.grid(row=0, column=0, padx=20, pady=20)
        self.SearchTextBox = Entry(self.parent)
        self.SearchTextBox.grid(row=1, column=0)
        self.searchBtn = Button(self.parent, text="Search", command=self.search_book_loans)
        self.searchBtn.grid(row=2, column=0)
        self.ResultTreeview = Treeview(self.parent, columns=4, show=['headings'])
        self.ResultTreeview["columns"] = ("1", "2","3","4")
        self.ResultTreeview.grid(row=3, column=0)
        self.ResultTreeview.heading('1', text="Loan ID")
        self.ResultTreeview.heading('2', text="ISBN")
        self.ResultTreeview.heading('3', text="Borrower ID")
        self.ResultTreeview.heading('4', text="Book Title")
        self.ResultTreeview.bind('<ButtonRelease-1>', self.select_book_for_checkin)
        self.checkInBtn = Button(self.parent, text="Check In", command=self.check_in)
        self.checkInBtn.grid(row=4, column=0)

    def search_book_loans(self):
        for item in self.ResultTreeview.get_children():
            self.ResultTreeview.delete(item)
        self.search_string = self.SearchTextBox.get()
        cursor = libraryDatabase.cursor()
        cursor.callproc(procname='sp_getBookDetails',args=[self.search_string])
        results = cursor.stored_results()

        for result in results:
            self.results = result.fetchall()

        for result in self.results:
            self.ResultTreeview.insert('', 'end', iid=result[0], text=result[0],
                values =(result[0],result[1],result[2],result[3]))
        
        cursor.close()

    def select_book_for_checkin(self, a):
        curItem = self.ResultTreeview.focus()
        self.bookForCheckInID = self.ResultTreeview.item(curItem)['text']

    def check_in(self):
        if self.bookForCheckInID is None:
            messagebox.showinfo("Attention!", "Select Book to Check In First!")
            return None
        print(self.bookForCheckInID)
        args = (self.bookForCheckInID,0)
        cursor = libraryDatabase.cursor()
        resultargs = cursor.callproc(procname='sp_checkInBooks',args=args)
        checkoutCode = resultargs[1]
        print(args)
        print("===========out==========",checkoutCode)
        if(checkoutCode == 200):
            messagebox.showinfo('Success', 'Book Checked In Successfully')