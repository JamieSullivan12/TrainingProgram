import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from Process_DataStructures import Trainee
import pandas as pd
import random

class AddTraineePage(ttk.Frame):
    def add_trainee(self):
        """
        Handles the generation of a new customer
        """

        # get the user defined name and email
        name = self.name_entry.get()
        email = self.email_entry.get()

        # edge case scenario for empty fields
        if name == "" or email == "":
            messagebox.showerror(message="Name or email are empty. Please make sure that they have a value before adding a trainee.")
            return # cancel add trainee operation

        # generate random six-digit identifier (and prevent the unlikely event of a duplicate)
        id = random.randint(99999,999999)
        while id in self.mainline_obj.customerdata_dict:
            id = random.randint(99999,999999)
        
        # instantiate a new object for the Trainee
        # note that this simply generates an empty Trainee object. It will be populated later
        new_trainee_obj = Trainee(self.mainline_obj,self.mainline_obj.customerdata_obj, self.mainline_obj.customerdata_obj.get_current_index())

        # call the Trainee method to insert data like the id, name and email
        new_trainee_obj.create_trainee_object(id, name, email)
        # add the newly created trainee to the dictionary in the mainline
        self.mainline_obj.customerdata_dict[id] = new_trainee_obj

        # to ensure changes take effect, reset all windows and show the home page
        self.mainline_obj.resetwindows()
        self.mainline_obj.showwindow("HomePage")
        return

    
    def __init__(self, mainline_obj):
        # mainline_obj refers to the object in which the mainline algorithm occurs
        # this contains any crucial data that needs to be able to be accessed from anywhere within the program - like datastructures or the top level frame
        self.mainline_obj = mainline_obj

        # instantiate a new frame object (placing it on the top-level scrollable_frame and extend it to this class)
        ttk.Frame.__init__(self, self.mainline_obj.scrollable_frame)

        # title widget
        title = ttk.Label(self, text="Add Trainee")
        title.grid(row=0,column=0, padx=20, pady=(15,0), sticky="w")

        # user entry widgets
        i=1
        self.name_label = ttk.Label(self, text="Name")
        self.name_entry = ttk.Entry(self, width=20)
        self.name_label.grid(row=i, column=0, padx=20, pady=(25,0), sticky="w")
        self.name_entry.grid(row=i+1,column=0, padx=20, pady=(5,10), sticky="w")
        i+=2
        self.email_label = ttk.Label(self, text="Email")
        self.email_entry = ttk.Entry(self, width=20)
        self.email_label.grid(row=i, column=0, padx=20, pady=(10,0),sticky="w")
        self.email_entry.grid(row=i+1,column=0, padx=20, pady=(5,10), sticky="w")
        i += 2
        
        # button links to page where a new customer can be created
        add_customer = ttk.Button(self, text='Add Trainee', command=lambda:self.add_trainee())
        add_customer.grid(row=i,column=0, padx=20, pady=10, sticky="w")
