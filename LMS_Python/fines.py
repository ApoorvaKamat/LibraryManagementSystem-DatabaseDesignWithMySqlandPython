from tkinter import *
from tkinter import simpledialog, messagebox
from tkinter.ttk import Treeview
import mysql.connector as sqlConn

from main import libraryDatabase

class Fines:
    def __init__(self, master):
        self.parent = master

        self.results = None
        self.borrowerCardId = None

        self.searchLabel = Label(self.parent, text="Welcome to Fines Manager")
        self.searchLabel.grid(row=0, column=0, padx=20, pady=20)
        self.generateFineBtn = Button(self.parent, text="Generate Fines", command=self.generate_fines)
        self.generateFineBtn.grid(row=1, column=0, padx=10, pady=10)
        self.buttonFrame = Frame(self.parent)
        self.buttonFrame.grid(row=2, column=0, sticky=N)
        self.buttonFrame.grid_rowconfigure(2, weight=1)
        self.viewAllFinesBtn = Button(self.buttonFrame, text="View All Fines", command=self.view_all_fines)
        self.viewAllFinesBtn.grid(row=0, column=0, padx=10, pady=10)
        self.viewAllFinesBtn.grid_rowconfigure(0, weight=1)
        self.viewAllFinesBtn.grid_columnconfigure(0, weight=1)
        self.viewPaidBtn = Button(self.buttonFrame, text="View Paid Fines", command=self.view_paid_fines)
        self.viewPaidBtn.grid(row=0, column=1,padx=10, pady=10)
        self.viewAllFinesBtn.grid_rowconfigure(0, weight=1)
        self.viewUnpaidbtn = Button(self.buttonFrame, text="View Unpaid Fines", command=self.view_unPaid_fines)
        self.viewUnpaidbtn.grid(row=0, column=2, padx=10, pady=10)
        self.viewAllFinesBtn.grid_rowconfigure(2, weight=1)
        self.ResultTreeview = Treeview(self.parent, columns=2, show=["headings"])
        self.ResultTreeview.grid(row=3, column=0)
        self.ResultTreeview["columns"] = ("1", "2")
        self.ResultTreeview.heading("1", text="Card ID")
        self.ResultTreeview.heading("2", text="Fine Amt")
        self.ResultTreeview.bind('<ButtonRelease-1>', self.select_borrower_card_id)
        self.checkInBtn = Button(self.parent, text="Update Fine", command=self.update_fine_for_borrower)
        self.checkInBtn.grid(row=4, column=0)


    def generate_fines(self):
        cursor = libraryDatabase.cursor()
        cursor = libraryDatabase.cursor()
        cursor.callproc(procname='sp_updateFines')
        messagebox.showinfo("Info", "Generated Fines")

    def select_borrower_card_id(self, a):
        curItem = self.ResultTreeview.focus()
        self.borrowerCardId = self.ResultTreeview.item(curItem)['text']

    def update_fine_for_borrower(self):
        if self.borrowerCardId is None:
            messagebox.showinfo("Errror", "Please select a borrower")
            return None
        args = (self.borrowerCardId,0)
        cursor = libraryDatabase.cursor()
        resultargs = cursor.callproc(procname='sp_updateFinesByCardId',args=args)
        checkoutCode = resultargs[1]
        print(args)
        print("===========out==========",checkoutCode)
        if(checkoutCode == 200):
            messagebox.showinfo('Success', 'Fines Updated Successfully')


    def view_all_fines(self):
        for item in self.ResultTreeview.get_children():
            self.ResultTreeview.delete(item)
        cursor = libraryDatabase.cursor()
        cursor.callproc(procname='sp_showFines')
        results = cursor.stored_results()

        for result in results:
            self.results = result.fetchall()

        for result in self.results:
            self.ResultTreeview.insert("", 'end',iid=result[0],text=result[0],
                values =(result[0],result[1]))
                
                
        cursor.close()

    def view_paid_fines(self):
        for item in self.ResultTreeview.get_children():
            self.ResultTreeview.delete(item)

        cursor = libraryDatabase.cursor()
        cursor.callproc(procname='sp_showPaidFines')
        results = cursor.stored_results()

        for result in results:
            self.results = result.fetchall()

        for result in self.results:
            self.ResultTreeview.insert("", 'end',iid=result[0],text=result[0],
                values =(result[0],result[1]))
        
        cursor.close()

    def view_unPaid_fines(self):
        for item in self.ResultTreeview.get_children():
            self.ResultTreeview.delete(item)

        cursor = libraryDatabase.cursor()
        cursor.callproc(procname='sp_showUnPaidFines')
        results = cursor.stored_results()

        for result in results:
            self.results = result.fetchall()

        for result in self.results:
            self.ResultTreeview.insert("", 'end',iid=result[0],text=result[0],
                values =(result[0],result[1]))
        
        
        cursor.close()