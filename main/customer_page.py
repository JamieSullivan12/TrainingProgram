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

        return table_array,customers


    '''
    FUNCTION: Save all changes the user has made in the customer table
    IN:
    - customer_df: pandas datastructure containing the raw data (written to if there is a change)
    - table_array: A 2D array of entry object (textboxes from the table). Accessed to see if the user has made changes
    OUT:
    - None
    '''
    def save_changes(self, table_array, customers):
        # library used when accessing the pandas library (column name required instead of index)
        
        save_log = ""
        changes_made = False
        cancel = False
        for c in customers:
            if cancel==False:

                error_msg,items_changed=customers[c].check_difference()
                
                if error_msg!="":cancel=True
                
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
           


        '''
        #loop through each row in the customer datastructure
        for i,values in self.controller.customer_df.iterrows():
            # loop through each column for each row in the customer datastructure
            for g,value in enumerate(values):
                value = str(value)
                # if the field being updated is a date, slightly more logic is required
                if self.indexes[g]=="DoB":
                    override_cont = False #used to overridde if old date is incorrect format (so it can be changed)
                    cancel = False # if the new date is incorrect, the change will be cancelled
                    old_datetime_object = "NaN"
                    new_datetime_object = "NaN"
                    try: # making the old date as a datetime object (this is the date that currently sits in the pandas dataset)
                        old_datetime_object = pd.to_datetime(str(value), format="%Y-%m-%d")
                    except ValueError as e:
                        override_cont = True
                    try: #making the new date as a datetime object (this is the date that the user entered). If it is incorrect, the change will be cancelled.
                        new_datetime_object = pd.to_datetime(str(table_array[i][g].get()), format="%d/%m/%Y")
                    except ValueError as e:
                        cancel = True
                        tkinter.messagebox.showerror(title="Unable to save changes", message=f"The date entered for {table_array[i][0].get()} is invalid. This customer will not be updated.")

                    if  override_cont or old_datetime_object != new_datetime_object and not cancel:
                        new_date = new_datetime_object
                        self.controller.customer_df.at[i,self.indexes[g]]=new_date
                        save_log += "Customer: " + table_array[i][0].get() + "; Column: " + self.indexes[g] + " -> '" + table_array[i][g].get() + "'\n"
                        changes_made = True
                
                else:
                    # only save the changes which exist
                    if value != table_array[i][g].get():
                        try:
                            #at the point (i - row,g - column), change the value to what currently sits in the corresponding textbox on the tkinter widget
                            self.controller.customer_df.at[i,self.indexes[g]]=str(table_array[i][g].get())
                            save_log += "Customer: " + table_array[i][0].get() + "; Column: " + self.indexes[g] + " -> '" + table_array[i][g].get() + "'\n"
                            changes_made = True #flag used at the end
                        except ValueError as e:
                            # a field cannot be empty because it will throw an error. revert the change if this occurs
                            tkinter.messagebox.showerror(title="Empty field invalid", message="Customer: " + table_array[i][0].get() + "; Column: " + self.indexes[g] + " - cannot be empty. Your change will now be reverted")
                            table_array[i][g].insert(tk.END,str(value))

        #logging and error message purposes
        if changes_made:
            try:
                self.controller.customer_df.to_csv("tempdata1.csv", index=False)
                tkinter.messagebox.showinfo(title="Successfully saved changes", message="Your changes were saved:\n\n" + save_log)
            except PermissionError as e:
                tkinter.messagebox.showerror(title="Unable to save changes", message="Please ensure that the core data file is not open and try again.")
            except Exception as e:
                tkinter.messagebox.showerror(title="Unable to save changes", message="Unknown error. Please try again and contact the administrator for support.")
        else:
            tkinter.messagebox.showinfo(title="No changes were made", message="No changes were made")
        '''
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
        table_array,customers = self.read_customer_data() 
        # to be used when the user changes any fields in the table on screen
        save_changes_button = tk.Button(self.frame, text='Save Changes',borderwidth=0,width=15, height=1,font=self.controller.p3, fg="#ffffff", bg=self.controller.buttonBackground,activebackground=self.controller.buttonClick,activeforeground="#ffffff", relief=tk.FLAT, command=lambda:self.save_changes(table_array, customers))
        save_changes_button.grid(row=0,column=1, padx=50, pady=15)
        controller.button_hover(save_changes_button,self.controller.buttonClick,self.controller.buttonBackground)

        # button links to page where a new customer can be created
        save_changes_button = tk.Button(self.frame, text='Add Customer',borderwidth=0,width=15, height=1,font=self.controller.p3, fg="#ffffff", bg=self.controller.buttonBackground,activebackground=self.controller.buttonClick,activeforeground="#ffffff", relief=tk.FLAT, command=lambda:self.controller.show_frame("AddCustomerPage"))
        save_changes_button.grid(row=0,column=2, padx=50, pady=15)
        controller.button_hover(save_changes_button,self.controller.buttonClick,self.controller.buttonBackground)

