# -------------------------------------------
# creates the home page once initialised
# -------------------------------------------

from tkinter import ttk

class HomePage(ttk.Frame):
    """Controls the GUI for HomePage"""
    
    def __init__(self, toplevel):
        # toplevel refers to the class in which the mainline algorithm occurs
        self.toplevel = toplevel

        # inherit ttk.Frame class - that means that the HomePage class WILL BECOME also a ttk.Frame class
        # self.toplevel.frame_obj.scrollable_frame refers to the frame on which this inherited frame will be placed
        ttk.Frame.__init__(self, self.toplevel.frame_obj.scrollable_frame)

    
        # Widgets
        heading = ttk.Label(self,text="Training App")
        heading.grid(row=0,column=0,sticky="nw",padx=35,pady=(20,0))
        
        self.traineesearch_button = ttk.Button(self,text="Trainee Search", width=30,command=lambda:self.toplevel.showwindow("CustomerPage"))
        self.traineesearch_button.grid(row=1,column=0, padx=(20,10),pady=10)

        self.addtrainee_button = ttk.Button(self,text="Add Trainee",width=30, command=lambda:self.toplevel.showwindow("AddCustomerPage"))
        self.addtrainee_button.grid(row=2,column=0, padx=(20,10),pady=10)

        self.addexercise_button = ttk.Button(self,text="Add Exercise",width=30, command=lambda:self.toplevel.showwindow("ModifyExercisesPage"))
        self.addexercise_button.grid(row=3,column=0, padx=(20,10),pady=10)

