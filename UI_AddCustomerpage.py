import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import pandas as pd

class AddCustomerPage(ttk.Frame):
    def set_heading(self):
        self.controller.tkRoot.title("Training App > Add Customer")

    def add_customer(self):
        cont = True
        name = self.name_entry.get()
        email = self.email_entry.get()
        try:
            DoB = pd.to_datetime(self.date_entry.get(), format="%d/%m/%Y")
        except ValueError as e:
            cont = False
            messagebox.showerror(title="Unable to save changes", message=f"Invalid date. Please enter in the format DD/MM/YYYY")

        if cont:
            try:
                new_row = {'Name': name, "DoB":DoB, "Email":email}
                self.controller.customer_df = self.controller.customer_df.append(new_row, ignore_index=True)
                self.controller.customer_df.to_csv("tempdata1.csv", index=False)
                messagebox.showinfo(title="Customer Added", message=f"{name} has been added!")
            except PermissionError as e:
                messagebox.showerror(title="Unable to save changes", message="Please ensure that the core data file is not open and try again.")
            except Exception as e:
                messagebox.showerror(title="Unable to save changes", message="Unknown error. Please try again and contact the administrator for support.")
        
        self.controller.setupwindows()
        self.controller.showwindow("CustomerPage")


    def __init__(self, controller):
        ttk.Frame.__init__(self, controller.frame_obj.scrollable_frame)

        self.indexes = {0:"Name",1:"DoB",2:"Goals",3:"Email"}

        self.controller = controller
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        title = ttk.Label(self, text="Customers")
        title.grid(row=0,column=0, padx=10, pady=(10,0), sticky="w")


        i=0
        self.name_label = ttk.Label(self, text="Name")
        self.name_entry = ttk.Entry(self, width=20)
        self.name_label.grid(row=i+1, column=0)
        self.name_entry.grid(row=i+2,column=0)

        i+=2
        self.date_label = ttk.Label(self, text="Date of Birth (DD/MM/YYYY)")
        self.date_entry = ttk.Entry(self, width=20)
        self.date_label.grid(row=i+1, column=0)
        self.date_entry.grid(row=i+2,column=0)

        i+=2
        self.email_label = ttk.Label(self, text="Email")
        self.email_entry = ttk.Entry(self, width=20)
        self.email_label.grid(row=i+1, column=0)
        self.email_entry.grid(row=i+2,column=0)

        i += 3
        
        # button links to page where a new customer can be created
        add_customer = ttk.Button(self, text='Add Customer', command=lambda:self.add_customer())
        add_customer.grid(row=i,column=0)
