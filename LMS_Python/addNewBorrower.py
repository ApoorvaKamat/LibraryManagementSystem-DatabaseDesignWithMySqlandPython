from tkinter import *
from tkinter import simpledialog, messagebox
from tkinter.ttk import Treeview
import mysql.connector as sqlConn

from main import libraryDatabase

class AddNewBorrower:
    def __init__(self, master):
        self.parent = master

        self.newCardID = None

        self.titleLabel = Label(self.parent, text="Enter Details")
        self.titleLabel.grid(row=0, column=0, padx=20, pady=20)
        self.fnameLabel = Label(self.parent, text="First Name").grid(row=1, column=0, padx=10, pady=5)
        self.fName = Entry(self.parent)
        self.fName.grid(row=2, column=0, padx=10, pady=5)
        self.lnameLabel = Label(self.parent, text="Last Name").grid(row=3, column=0, padx=10, pady=5)
        self.lName = Entry(self.parent)
        self.lName.grid(row=4, column=0, padx=10, pady=5)
        self.ssnLabel = Label(self.parent, text="SSN").grid(row=5, column=0, padx=10, pady=5)
        self.ssn = Entry(self.parent)
        self.ssn.grid(row=6, column=0, padx=10, pady=5)
        self.addressLabel = Label(self.parent, text="Street Address").grid(row=7, column=0, padx=10, pady=5)
        self.address = Entry(self.parent)
        self.address.grid(row=8, column=0, padx=10, pady=5)
        self.cityLabel = Label(self.parent, text="City").grid(row=9, column=0, padx=10, pady=5)
        self.city = Entry(self.parent)
        self.city.grid(row=10, column=0, padx=10, pady=5)
        self.stateLabel = Label(self.parent, text="State").grid(row=11, column=0, padx=10, pady=5)
        self.state = Entry(self.parent)
        self.state.grid(row=12, column=0, padx=10, pady=5)
        self.numberLabel = Label(self.parent, text="Phone Number").grid(row=13, column=0, padx=10, pady=5)
        self.phoneNumber = Entry(self.parent)
        self.phoneNumber.grid(row=14, column=0, padx=10, pady=5)
        self.addBorrowerBtn = Button(self.parent, text="Add Borrower", command=self.add_borrower)
        self.addBorrowerBtn.grid(row=15, column=0, padx=10, pady=10)

    def add_borrower(self):
        args = (self.fName.get(),
                self.lName.get(),
                self.ssn.get(),
                self.address.get(),
                self.city.get(),
                self.state.get(),
                self.phoneNumber.get(),
                0)
        cursor = libraryDatabase.cursor()
        resultargs = cursor.callproc(procname='sp_addNewBorrower',args=args)
        reslts = cursor.stored_results()
        checkoutCode = resultargs[7]
        print(args)
        print("===========out==========",checkoutCode)
        for result in reslts:
            arr = result.fetchall()
            self.newCardID = arr[0]
            print(self.newCardID)
        match checkoutCode:
            case 500: 
                messagebox.showinfo("Error", "SSN already exits")
                return NONE
            case 200:
                message = "Borrower Added successfully with card Id : " + str(self.newCardID)
                print (message)
                messagebox.showinfo("Add Success", message)
                self.parent.destroy()
               
                