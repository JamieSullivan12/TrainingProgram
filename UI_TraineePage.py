
from encodings import search_function
import tkinter as tk
from tkinter import ttk
import main
import tkinter.messagebox
import pandas as pd
from datetime import datetime,date


'''
Contains the code for the customer page. On this page, the user can access all customer details and change them
'''
class CustomerPage(ttk.Frame):

    """
    Object containing only information for each customer row seen in the customers user interface page
    """
    class CustomerRow(): 
        def customer_moreinfo(self,event):
            """
            Injects data for this customer object into the MoreInfoPage (using abstracted function .injectdata). Then switches
            to that page using the showwindow function from app.py
            """
            self.controller.controller.frames["MoreInfoPage"].injectdata(self.customer)
            self.controller.controller.showwindow("MoreInfoPage")
        def bindframe(self,frame,sequence,func):
            frame.bind(sequence, func)
            for child in frame.winfo_children():
                child.bind(sequence, func)
        def __init__(self,controller,row_num,customer):
            self.customer=customer
            self.controller=controller

            # creating child frame in which individual customer rows will appear
            self.customer_frame = ttk.Frame(self.controller)
            self.customer_frame.columnconfigure(0, weight=3)
            self.customer_frame.columnconfigure(1, weight=1)
            # horizontal line separating customer rows
            self.bottom_seperator = ttk.Separator(self.customer_frame,orient='horizontal')

            # customer name and date of birth
            self.name_label = ttk.Label(self.customer_frame,text=customer.name)
            self.name_label.grid(row=0, column=0, padx=(20,60),pady=20)
            self.email_label = ttk.Label(self.customer_frame, text=f"{customer.email}")
            self.email_label.grid(row=0, column=1)

            self.bottom_seperator.grid(row=2,column=0,columnspan=100,sticky="ew")
            self.customer_frame.grid(row=row_num,column=0,columnspan=100,sticky="ew",padx=40)

            # on double click, run the more info function (see function pydocs)
            self.bindframe(self.customer_frame,"<Double-Button-1>",self.customer_moreinfo)




    def save_changes(self, customers):
        '''
        FUNCTION: Save all changes the user has made in the customer table
        IN:
        - customers: A list of all the customer objects
        OUT:
        - None
        '''

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
                    save_log+=f"Trainee: {customers[c].name} updated.\n"

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
    

    def searchfunction(self):
        """
        Prints all customers in the database. Will only include what is in the searchbox (defined class initialisation).
        NOTE: if searchbox is empty, the filter will include all customers
        """
        search_filter = self.search_texbox.get()

        # remove all current customer rows printed on screen (they will be replaced)
        for row in self.listofrows:
            row.customer_frame.grid_forget()
        self.listofrows=[]
        
        # incremental value to print each customer on a new row in the tkinter window
        row_num=2
        # for each customer in the dataset, if it satisfies the search requirements, initialise and append the new customer row to a list
        for customer in self.controller.customerdata_dict:
            if search_filter=="" or search_filter.lower() in self.controller.customerdata_dict[customer].name.lower() or search_filter.lower() in self.controller.customerdata_dict[customer].email.lower():
                self.listofrows.append(self.CustomerRow(self,row_num,self.controller.customerdata_dict[customer]))
                row_num+=1



    def __init__(self, controller):
        ttk.Frame.__init__(self, controller.frame_obj.scrollable_frame)
        self.controller = controller

        title = ttk.Label(self, text="Trainee Search")
        title.grid(row=0,column=0, padx=(40,10), pady=(10,0), sticky="w")


        self.search_texbox = ttk.Entry(self, width=50)
        self.search_texbox.grid(row=1,column=0,padx=(40,0))
        self.search_button = ttk.Button(self,text="Search", width=30,command=lambda:self.searchfunction())
        self.search_button.grid(row=1,column=1, padx=(20,10),pady=10)

        # used to store all customer row objects
        self.listofrows=[]
        self.searchfunction()
