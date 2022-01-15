import tkinter as tk
from datetime import datetime

class Customers():
    def __init__(self, id, name, DoB, goals, email, pandas_index):
        self.id = id
        self.name = name
        self.DoB = DoB
        self.goals = goals
        self.email = email
        self.pandas_index = pandas_index
    
    '''
    FUNCTION: Add a set of tkinter textbox objects to each contract. Used to access the value of any changes the user has typed into those textboxes
    '''
    def add_table_row(self, name_textbox,DoB_textbox,goals_textbox,email_textbox):
        self.name_textbox=name_textbox
        self.DoB_textbox=DoB_textbox
        self.goals_textbox=goals_textbox
        self.email_textbox=email_textbox
        
    '''
    FUNCTION: To check whether any of the textboxes contain difference values from what is currently stored in the object
                if changes are found, then update the customer
    '''
    def check_difference(self):
        error_msg = ""
        changed = False
        items_changed = []
        
        # check whether current name value is different from what is in the textbox
        if self.name != self.name_textbox.get():
            changed = True
            self.name=self.name_textbox.get()
            items_changed.append("Name")
        
        # same as above, however the date field requires a validity check
        try:
            if changed==False and self.DoB != datetime.strptime(self.DoB_textbox.get(), '%d/%m/%Y'):
                changed = True
                self.DoB=datetime.strptime(self.DoB_textbox.get(), '%d/%m/%Y')
                items_changed.append("DoB")
        except Exception as e:
            error_msg+=f"{self.name}: date field is invalid\n"

        if changed==False and self.goals != self.goals_textbox.get():
            changed = True
            self.goals=self.goals_textbox.get()
            items_changed.append("Goals")
        if changed==False and self.email != self.email_textbox.get():
            changed = True
            self.email=self.email_textbox.get()
            items_changed.append("Email")
        
        return error_msg,items_changed