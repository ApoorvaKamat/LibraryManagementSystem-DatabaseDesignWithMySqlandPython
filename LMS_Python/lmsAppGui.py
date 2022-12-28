from tkinter import *
from tkinter import simpledialog, messagebox
from tkinter.ttk import Treeview
import mysql.connector as sqlConn

from main import libraryDatabase
from checkInBook import *
from addNewBorrower import *
from fines import *

class LmsAppGui:
    def __init__(self,master):
        self.parent = master

        #Initializations
        self.search_string = None
        self.results = None
        self.bookForCheckOutIsbn = None

        self.parent.title("Library Management System")
        self.frame = Frame(self.parent, width=900, height=750)
        self.frame.grid(row=0, column=0)
        self.frame.grid_rowconfigure(0, weight=2)
        self.frame.grid_columnconfigure(0, weight=2)
        # self.frame.grid_propagate(False)

         # Search Frame
        self.SearchFrame = Frame(self.frame)
        self.SearchFrame.grid(row=0, column=0, sticky=N)
        self.SearchFrame.grid_rowconfigure(1, weight=1)
        # self.SearchFrame.grid_columnconfigure(0, weight=1)
        self.SearchLabel = Label(self.SearchFrame, text='Search here: ISBN, Title, Author')
        self.SearchLabel.grid(row=0, column=0)
        self.SearchLabel.grid_rowconfigure(0, weight=1)
        # self.SearchLabel.grid_columnconfigure(0, weight=1)
        self.SearchTextBox = Entry(self.SearchFrame, text='Enter search string here...', width=50)
        self.SearchTextBox.grid(row=1, column=0)
        self.SearchTextBox.grid_rowconfigure(1, weight=1)
        self.SearchButton = Button(self.SearchFrame, text='Search', command=self.search)
        self.SearchButton.grid(row=1, column=2)
        self.SearchButton.grid_rowconfigure(2, weight=1)

        # Search Result Frame
        self.ResultArea = Frame(self.frame)
        self.ResultArea.grid(row=1, column=0, sticky=N)
        self.ResultArea.grid_rowconfigure(1, weight=1)
        self.ResultTreeview = Treeview(self.ResultArea, columns=4,show=["headings"])
        self.ResultTreeview.grid(row=1, column=1)
        self.ResultTreeview["columns"] = ("1", "2","3","4")
        self.ResultTreeview.grid_rowconfigure(0, weight=1)
        self.ResultTreeview.heading('1', text="ISBN")
        self.ResultTreeview.heading('2', text="Book Title")
        self.ResultTreeview.heading('3', text="Author(s)")
        self.ResultTreeview.heading('4', text="Availability")
        self.ResultTreeview.bind('<ButtonRelease-1>', self.selectBookForCheckout)

        # Interaction Frame
        self.ButtonFrames = Frame(self.frame)
        self.ButtonFrames.grid(row=3, column=0, sticky=N)
        self.ButtonFrames.grid_rowconfigure(3, weight=1)
        self.checkOutBtn = Button(self.ButtonFrames, text="Check Out Book", command=self.check_out)
        self.checkOutBtn.grid(row=0, column=0, padx=10, pady=10)
        self.checkOutBtn.grid_rowconfigure(0, weight=1)
        self.checkOutBtn.grid_columnconfigure(0, weight=1)
        self.checkInBtn = Button(self.ButtonFrames, text="Check In Book", command=self.check_in)
        self.checkInBtn.grid(row=0, column=1, padx=10, pady=10)
        self.checkInBtn.grid_rowconfigure(0, weight=1)
        self.checkInBtn.grid_columnconfigure(1, weight=1)
        self.addBorrowerBtn = Button(self.ButtonFrames, text="Add New Borrower", command=self.add_borrower)
        self.addBorrowerBtn.grid(row=0, column=2, padx=10, pady=10)
        self.payFinesBtn = Button(self.ButtonFrames, text="Fines Manager", command=self.pay_fines)
        self.payFinesBtn.grid(row=1, column=1, padx=10, pady=10)

    def search(self):
        for item in self.ResultTreeview.get_children():
            self.ResultTreeview.delete(item)
        self.search_string = self.SearchTextBox.get()
        cursor = libraryDatabase.cursor()
        cursor.callproc(procname='get_book_info_from_search',args=[self.search_string])
        results = cursor.stored_results()

        for result in results:
            self.results = result.fetchall()

        for result in self.results:
            self.ResultTreeview.insert('', 'end', iid=result[0], text=result[0],
                values =(result[0],result[1],result[2],result[3]))
        
        cursor.close()

    def selectBookForCheckout(self,a):
        curItem = self.ResultTreeview.focus()
        self.bookForCheckOutIsbn = self.ResultTreeview.item(curItem)['text']
    
    def check_out(self):
    #     -- ERROR CODES
    #       -- 501 BOOK NOT FOUND
    #       -- 502 CARD ID NOT FOUND
    #       -- 200 BOOK CHECK OUT SUCCESS
    #       -- 400 BOOK NOT AVAILABLE FOR CHCEKOUT
    #       -- 600 3 BOOKS CHECKED OUT 
        if self.bookForCheckOutIsbn is None:
            messagebox.showinfo("Attention!", "Select Book First!")
            return None
        self.borrowerId = simpledialog.askstring("Check Out Book", "Please Enter Card ID")

        args = (self.bookForCheckOutIsbn,self.borrowerId,0)
        cursor = libraryDatabase.cursor()
        resultargs = cursor.callproc(procname='sp_checkOutBooks',args=args)
        checkoutCode = resultargs[2]
        print(args)
        print("===========out==========",checkoutCode)

        match checkoutCode:
            case 501:
                messagebox.showinfo("Not Allowed!", "BOOK NOT FOUND")
                return None
            case 502:
                messagebox.showinfo("Error", "CARD ID NOT FOUND")
                return None
            case 400:
                messagebox.showinfo("Not Allowed!", "BOOK NOT AVAILABLE FOR CHCEKOUT")
                return None
            case 600:
                messagebox.showinfo("Not Allowed!", "BORROWER HAS 3 BOOKS CHECKED OUT")
                return None
            case 200:
                messagebox.showinfo("Success","Book Checkout Successfull")

    def  check_in(self):
        self.checkInWindow = Toplevel(self.parent)
        self.checkInWindow.title("LMS Check In")
        self.app = CheckInBook(self.checkInWindow)   
    
    def add_borrower(self):
        self.newBorrowerWindow = Toplevel(self.parent)
        self.newBorrowerWindow.title("Add New Borrower Details")
        self.newapp = AddNewBorrower(self.newBorrowerWindow)

    def pay_fines(self):
        self.newPayFinesWindow = Toplevel(self.parent)
        self.newPayFinesWindow.title("Fines Manager")
        self.app1 = Fines(self.newPayFinesWindow)