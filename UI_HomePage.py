# -------------------------------------------
# creates the home page once initialised
# -------------------------------------------

from tkinter import ttk

class HomePage(ttk.Frame):
    """Controls the GUI for HomePage"""
    
    def __init__(self, controller):
        # inherit ttk.Frame class - that means that the HomePage class WILL BECOME also a ttk.Frame class
        ttk.Frame.__init__(self, controller.frame_obj.scrollable_frame)

        self.controller = controller

        # place widgets on the screen (title & buttons)
        header = ttk.Label(self,text="Training App")
        header.grid(row=0,column=0,sticky="nw",padx=35,pady=(20,0))
        
        self.customers_button = ttk.Button(self,text="Customers", width=30,command=lambda:self.controller.showwindow("CustomerPage"))
        self.customers_button.grid(row=1,column=0, padx=(20,10),pady=10)

        self.add_customer_button = ttk.Button(self,text="Add Customer",width=30, command=lambda:self.controller.showwindow("AddCustomerPage"))
        self.add_customer_button.grid(row=2,column=0, padx=(20,10),pady=10)

        self.modify_exercises_button = ttk.Button(self,text="Modify Exercises Dataset",width=30, command=lambda:self.controller.showwindow("ModifyExercisesPage"))
        self.modify_exercises_button.grid(row=3,column=0, padx=(20,10),pady=10)

