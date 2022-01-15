import main
import tkinter as tk
import tkinter.messagebox
import pandas as pd
from datetime import datetime,date
from datastructures import Customers

'''
Contains the code for the customer page. On this page, the user can access all customer details and change them
'''
class CustomerPage(tk.Frame):

    '''
    Function: Read customer data from temporary CSV file (which is downloaded and later uploaded to the cloud). Create the table on the TKinter page
    IN:
    - self
    OUT:
    - customer_df: the pandas datastructure containing customer data
    - table_array: a 2D array of all the text boxes in the grid on the tkinter window
    '''
    def read_customer_data(self):

        indexes = {}
        # print all the headers across the screen at the top (will reference each column in the table created below)
        for l,header in enumerate(list(self.controller.customer_df)): #list(customer_df) returns all headings
            indexes[header]=l

        for g, heading in enumerate(["Name","Date Of Birth","Goals","Email"]):
            col_heading = tk.Label(self.frame, text=heading, bg=self.controller.backgroundColor, fg='black', font=self.controller.p1)
            if g==0:col_heading.grid(row=1,column=g, padx=(10,0), pady=(10,0), sticky="w")
            else:col_heading.grid(row=1,column=g, pady=(10,0), sticky="w")

        customers = {}
        table_array = []
        # loop through each row of datastructure
        for i,values in self.controller.customer_df.iterrows():

            name = values[indexes["Name"]]
            DoB = values[indexes["DoB"]]
            goals = values[indexes["Goals"]]
            email = values[indexes["Email"]]
            id = values[indexes["ID"]]

            c = Customers(id,name,DoB,goals,email,i)
            customers[id]=c

            self.name_textbox = tk.Entry(self.frame, width=20, fg='blue',font=("Arial",16,"bold"))
            self.name_textbox.insert(tk.END, name)
            self.name_textbox.grid(row=i+2,column=0, padx=(10,0))
            self.DoB_textbox = tk.Entry(self.frame, width=20, fg='blue',font=("Arial",16,"bold"))
            self.DoB_textbox.insert(tk.END, f'{DoB.day}/{DoB.month}/{DoB.year}')
            self.DoB_textbox.grid(row=i+2,column=1)
            self.goals_textbox = tk.Entry(self.frame, width=20, fg='blue',font=("Arial",16,"bold"))
            self.goals_textbox.insert(tk.END, goals)
            self.goals_textbox.grid(row=i+2,column=2)
            self.email_textbox = tk.Entry(self.frame, width=20, fg='blue',font=("Arial",16,"bold"))
            self.email_textbox.insert(tk.END, email)
            self.email_textbox.grid(row=i+2,column=3)

            c.add_table_row(self.name_textbox,self.DoB_textbox,self.goals_textbox,self.email_textbox)

            table_array.append([self.name_textbox,self.DoB_textbox,self.goals_textbox,self.email_textbox])

        return customers


    '''
    FUNCTION: Save all changes the user has made in the customer table
    IN:
    - customers: A list of all the customer objects
    OUT:
    - None
    '''
    def save_changes(self, customers):

        save_log = ""
        cancel = False

        for c in customers:
            if cancel==False: #break value
                # customer object method to check if changes have been made
                error_msg,items_changed=customers[c].check_difference()
                if error_msg!="":cancel=True # if an error occured when checking the differences, break out of the loop
                #if no errors occured, update all the values for that customer
                elif len(items_changed)>0 and error_msg=="":
                
                    self.controller.customer_df.at[customers[c].pandas_index,"Name"]=customers[c].name
                    self.controller.customer_df.at[customers[c].pandas_index,"DoB"]=customers[c].DoB
                    self.controller.customer_df.at[customers[c].pandas_index,"Goals"]=customers[c].goals
                    self.controller.customer_df.at[customers[c].pandas_index,"Email"]=customers[c].email
                    save_log+=f"Customer: {customers[c].name} updated.\n"

        if save_log=="" and error_msg=="":
            tkinter.messagebox.showinfo(title="No changes were made", message="No changes were made")
        elif save_log=="" and error_msg!="":
            tkinter.messagebox.showerror(title="An Error Occured!", message=error_msg)
        elif save_log!="":                
            self.controller.customer_df.to_csv("tempdata1.csv", index=False)
            try:
                self.controller.customer_df.to_csv("tempdata1.csv", index=False)
                tkinter.messagebox.showinfo(title="Successfully saved changes", message="Your changes were saved:\n\n" + save_log)
            except PermissionError as e:
                tkinter.messagebox.showerror(title="Unable to save changes", message="Please ensure that the core data file is not open and try again.")
           

    def set_heading(self):
        self.controller.tkRoot.title("Training App > Customers")

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

        # read data and create table
        customers = self.read_customer_data() 
        # to be used when the user changes any fields in the table on screen
        save_changes_button = tk.Button(self.frame, text='Save Changes',borderwidth=0,width=15, height=1,font=self.controller.p3, fg="#ffffff", bg=self.controller.buttonBackground,activebackground=self.controller.buttonClick,activeforeground="#ffffff", relief=tk.FLAT, command=lambda:self.save_changes(customers))
        save_changes_button.grid(row=0,column=1, padx=50, pady=15)
        controller.button_hover(save_changes_button,self.controller.buttonClick,self.controller.buttonBackground)

        # button links to page where a new customer can be created
        save_changes_button = tk.Button(self.frame, text='Add Customer',borderwidth=0,width=15, height=1,font=self.controller.p3, fg="#ffffff", bg=self.controller.buttonBackground,activebackground=self.controller.buttonClick,activeforeground="#ffffff", relief=tk.FLAT, command=lambda:self.controller.show_frame("AddCustomerPage"))
        save_changes_button.grid(row=0,column=2, padx=50, pady=15)
        controller.button_hover(save_changes_button,self.controller.buttonClick,self.controller.buttonBackground)

