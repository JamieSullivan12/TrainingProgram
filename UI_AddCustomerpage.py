import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from Process_DataStructures import Trainee
import pandas as pd
import random

class AddCustomerPage(ttk.Frame):
    def add_customer(self):
        new_trainee_obj = Trainee(self.controller,self.controller.customerdata_obj.cusomter_pd, self.controller.customerdata_obj.get_current_index())

        name = self.name_entry.get()
        email = self.email_entry.get()

        id = random.randint(0,999999)
        
        while id in self.controller.customerdata_dict:
            id = random.randint(0,999999)
        
        new_trainee_obj.create_trainee_object(id, name, email)
        self.controller.customerdata_dict[id] = new_trainee_obj

        self.controller.setupwindows()
        self.controller.showwindow("HomePage")
    def __init__(self, controller):
        ttk.Frame.__init__(self, controller.frame_obj.scrollable_frame)

        self.indexes = {0:"Name",1:"DoB",2:"Goals",3:"Email"}

        self.controller = controller
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        title = ttk.Label(self, text="Add Trainee")
        title.grid(row=0,column=0, padx=20, pady=(15,0), sticky="w")


        i=0
        self.name_label = ttk.Label(self, text="Name")
        self.name_entry = ttk.Entry(self, width=20)
        self.name_label.grid(row=i+1, column=0, padx=20, pady=(25,0), sticky="w")
        self.name_entry.grid(row=i+2,column=0, padx=20, pady=(5,10), sticky="w")

        i+=2
        self.email_label = ttk.Label(self, text="Email")
        self.email_entry = ttk.Entry(self, width=20)
        self.email_label.grid(row=i+1, column=0, padx=20, pady=(10,0),sticky="w")
        self.email_entry.grid(row=i+2,column=0, padx=20, pady=(5,10), sticky="w")

        i += 3
        
        # button links to page where a new customer can be created
        add_customer = ttk.Button(self, text='Add Customer', command=lambda:self.add_customer())
        add_customer.grid(row=i,column=0, padx=20, pady=10, sticky="w")
