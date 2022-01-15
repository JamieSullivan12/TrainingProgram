import tkinter as tk
from tkinter import messagebox
import main
import pandas as pd

class AddCustomerPage(tk.Frame):
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
        
        self.controller.create_frames()
        self.controller.show_frame("CustomerPage")


    def __init__(self, parent, controller):
            self.indexes = {0:"Name",1:"DoB",2:"Goals",3:"Email"}
            # initial setup
            tk.Frame.__init__(self, parent)
            self.controller = controller
            frame_obj = main.CreateScrollableFrame(self, self.controller)
            self.frame = self.scrollable_frame
            self.frame.grid_columnconfigure(0, weight=1)
            self.frame.grid_rowconfigure(0, weight=1)
            title = tk.Label(self.frame, text="Customers", bg=self.controller.backgroundColor, fg='black', font=controller.h2)
            title.grid(row=0,column=0, padx=10, pady=(10,0), sticky="w")


            i=0
            self.name_label = tk.Label(self.frame, text="Name", bg=self.controller.backgroundColor, fg='black', font=self.controller.p1)
            self.name_entry = tk.Entry(self.frame, width=20, fg='blue',font=("Arial",16,"bold"))
            self.name_label.grid(row=i+1, column=0)
            self.name_entry.grid(row=i+2,column=0)

            i+=2
            self.date_label = tk.Label(self.frame, text="Date of Birth (DD/MM/YYYY)", bg=self.controller.backgroundColor, fg='black', font=self.controller.p1)
            self.date_entry = tk.Entry(self.frame, width=20, fg='blue',font=("Arial",16,"bold"))
            self.date_label.grid(row=i+1, column=0)
            self.date_entry.grid(row=i+2,column=0)

            i+=2
            self.email_label = tk.Label(self.frame, text="Email", bg=self.controller.backgroundColor, fg='black', font=self.controller.p1)
            self.email_entry = tk.Entry(self.frame, width=20, fg='blue',font=("Arial",16,"bold"))
            self.email_label.grid(row=i+1, column=0)
            self.email_entry.grid(row=i+2,column=0)

            i += 3
            
            # button links to page where a new customer can be created
            add_customer = tk.Button(self.frame, text='Add Customer',borderwidth=0,width=15, height=1,font=self.controller.p3, fg="#ffffff", bg=self.controller.buttonBackground,activebackground=self.controller.buttonClick,activeforeground="#ffffff", relief=tk.FLAT, command=lambda:self.add_customer())
            add_customer.grid(row=i,column=0)
            controller.button_hover(add_customer,self.controller.buttonClick,self.controller.buttonBackground)