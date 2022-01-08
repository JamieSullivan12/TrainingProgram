import main
import tkinter as tk
import tkinter.messagebox
import pandas as pd
from datetime import datetime,date

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
        # create datastructure from raw data using pandas
        customer_df = pd.read_csv("tempdata1.csv")
        customer_df = customer_df.fillna('') #replace empty fields (which would normally show NaN) with ""
        customer_df['DoB'] = pd.to_datetime(customer_df['DoB'], dayfirst=True, errors='coerce')

        # print all the headers across the screen at the top (will reference each column in the table created below)
        for l,header in enumerate(list(customer_df)): #list(customer_df) returns all headings
            col_heading = tk.Label(self.frame, text=header, bg=self.controller.backgroundColor, fg='black', font=self.controller.p1)
            # only add padding to first element
            if l==0:col_heading.grid(row=1,column=l, padx=(10,0), pady=(10,0), sticky="w")
            else:col_heading.grid(row=1,column=l, pady=(10,0), sticky="w")


        table_array = []
        # loop through each row of datastructure
        for i,values in customer_df.iterrows():
            sub_table_array = []
            # loop through each column of each row
            for g,value in enumerate(values):
                # create the textbox in which the customer data field will be stored
                self.e = tk.Entry(self.frame, width=20, fg='blue',font=("Arial",16,"bold"))
                # add the textbox to the screen (10px padding on the first column of each row)
                if g == 0: self.e.grid(row=i+2,column=g, padx=(10,0))
                else: self.e.grid(row=i+2,column=g)
                
                if self.indexes[g]=="DoB":
                    self.e.insert(tk.END, f'{value.day}/{value.month}/{value.year}')
                else:
                    # insert the data into the respective box
                    self.e.insert(tk.END,str(value))
                sub_table_array.append(self.e)
            table_array.append(sub_table_array)
        return customer_df, table_array


    '''
    FUNCTION: Save all changes the user has made in the customer table
    IN:
    - customer_df: pandas datastructure containing the raw data (written to if there is a change)
    - table_array: A 2D array of entry object (textboxes from the table). Accessed to see if the user has made changes
    OUT:
    - None
    '''
    def save_changes(self,customer_df, table_array):
        # library used when accessing the pandas library (column name required instead of index)
        
        save_log = ""
        changes_made = False
        #loop through each row in the customer datastructure
        for i,values in customer_df.iterrows():
            # loop through each column for each row in the customer datastructure
            for g,value in enumerate(values):
                value = str(value)
                print(self.indexes[g]=="DoB")
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
                        customer_df.at[i,self.indexes[g]]=new_date
                        save_log += "Customer: " + table_array[i][0].get() + "; Column: " + self.indexes[g] + " -> '" + table_array[i][g].get() + "'\n"
                        changes_made = True
                
                else:
                    # only save the changes which exist
                    if value != table_array[i][g].get():
                        try:
                            #at the point (i - row,g - column), change the value to what currently sits in the corresponding textbox on the tkinter widget
                            customer_df.at[i,self.indexes[g]]=str(table_array[i][g].get())
                            save_log += "Customer: " + table_array[i][0].get() + "; Column: " + self.indexes[g] + " -> '" + table_array[i][g].get() + "'\n"
                            changes_made = True #flag used at the end
                        except ValueError as e:
                            # a field cannot be empty because it will throw an error. revert the change if this occurs
                            tkinter.messagebox.showerror(title="Empty field invalid", message="Customer: " + table_array[i][0].get() + "; Column: " + indexes[g] + " - cannot be empty. Your change will now be reverted")
                            table_array[i][g].insert(tk.END,str(value))

        #logging and error message purposes
        if changes_made:
            try:
                customer_df.to_csv("tempdata1.csv", index=False)
                tkinter.messagebox.showinfo(title="Successfully saved changes", message="Your changes were saved:\n\n" + save_log)
            except PermissionError as e:
                tkinter.messagebox.showerror(title="Unable to save changes", message="Please ensure that the core data file is not open and try again.")
            except Exception as e:
                tkinter.messagebox.showerror(title="Unable to save changes", message="Unknown error. Please try again and contact the administrator for support.")
        else:
            tkinter.messagebox.showinfo(title="No changes were made", message="No changes were made")

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
        customer_df, table_array = self.read_customer_data() 
        # to be used when the user changes any fields in the table on screen
        save_changes_button = tk.Button(self.frame, text='Save Changes',borderwidth=0,width=15, height=1,font=self.controller.p3, fg="#ffffff", bg=self.controller.buttonBackground,activebackground=self.controller.buttonClick,activeforeground="#ffffff", relief=tk.FLAT, command=lambda:self.save_changes(customer_df, table_array))
        save_changes_button.grid(row=0,column=2, columnspan=3, padx=50, pady=15)
        controller.button_hover(save_changes_button,self.controller.buttonClick,self.controller.buttonBackground)

