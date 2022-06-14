from tkinter import ttk

class HomePage(ttk.Frame):
    """Controls the GUI for HomePage"""
    
    def __init__(self, mainline_obj):
        # mainline_obj refers to the object in which the mainline algorithm occurs
        # this contains any crucial data that needs to be able to be accessed from anywhere within the program - like datastructures or the top level frame
        self.mainline_obj = mainline_obj

        # instantiate a new frame object (placing it on the top-level scrollable_frame and extend it to this class)
        ttk.Frame.__init__(self, self.mainline_obj.scrollable_frame)
    
        # Widgets
        heading = ttk.Label(self,text="Training App")
        heading.grid(row=0,column=0,sticky="nw",padx=35,pady=(20,0))
        
        self.traineesearch_button = ttk.Button(self,text="Trainee Search", width=30,command=lambda:self.mainline_obj.showwindow("CustomerPage"))
        self.traineesearch_button.grid(row=1,column=0, padx=(20,10),pady=10)

        self.addtrainee_button = ttk.Button(self,text="Add Trainee",width=30, command=lambda:self.mainline_obj.showwindow("AddTraineePage"))
        self.addtrainee_button.grid(row=2,column=0, padx=(20,10),pady=10)

        self.addexercise_button = ttk.Button(self,text="Add Exercise",width=30, command=lambda:self.mainline_obj.showwindow("ModifyExercisesPage"))
        self.addexercise_button.grid(row=3,column=0, padx=(20,10),pady=10)

