from cgitb import text
import tkinter as tk
from tkinter import ttk
import createtrainingplan
class MoreInfoPage(tk.Frame):
    
    class GoalsInput():
        def __init__(self,parent,name,row,column):
            self.label = ttk.Label(parent.frame, text=name)
            self.entry = ttk.Entry(parent.frame, width=20)
            self.label.grid(row=row, column=column)
            self.entry.grid(row=row+1,column=column)


    def injectdata(self,customer):
        self.customer=customer
        self.title["text"]=f"Customer: {self.customer.name}"
        self.DoB_label["text"]=f"Date of Birth: {self.customer.DoB}"
        self.Email_Label["text"]=f"Email: {self.customer.email}"
        for checkbutton_id in self.checkbuttons:
            self.checkbuttons[checkbutton_id][1].set(0)
        for category in self.customer.categories:
            self.checkbuttons[category][1].set(1)
    
    def update_goals(self):
        category_list = []
        for category_id in self.checkbuttons:
            if self.checkbuttons[category_id][1].get()==1:
                category_list.append(category_id)
        self.customer.categories = category_list
        self.customer.writetofile()

    def create_sessionplan(self):
        sessioncreator_obj = createtrainingplan.TrainingPlanCreator(self.customer, self.controller)
        sessioncreator_obj.createtrainingplan()

    def set_heading(self):
        self.controller.tkRoot.title("Training App > Edit Customer Data")
    def __init__(self, controller):
        # initial setup
        tk.Frame.__init__(self)
        self.controller = controller

        self.frame = ttk.Frame(self.controller.frame_obj.scrollable_frame)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)
        self.title = ttk.Label(self.frame, text=f"Customer: ")
        self.title.grid(row=0,column=0, padx=10, pady=(10,0), sticky="w")

        self.customerinfo_frame = ttk.LabelFrame(self.frame, text="Customer Information")
        self.DoB_label = ttk.Label(self.customerinfo_frame, text=f"Date of Birth: ")
        self.DoB_label.grid(row=0,column=0, padx=10, pady=15, sticky="w")
        self.Email_Label = ttk.Label(self.customerinfo_frame, text=f"Email: ")
        self.Email_Label.grid(row=1,column=0, padx=10, pady=15, sticky="w")
        self.customerinfo_frame.grid(row=1,column=0,padx=20,pady=20)

        self.checkbuttons={}
        self.goalscheckbutton_frames = ttk.LabelFrame(self.frame, text="Customer Goals")
        for category in self.controller.categorydata_dict:
            CheckVar = tk.IntVar()

            checkbutton = ttk.Checkbutton(self.goalscheckbutton_frames,
                text=self.controller.categorydata_dict[category].category,
                variable=CheckVar,
                command=self.update_goals,
                onvalue=1,
                offvalue=0)
            checkbutton.pack(anchor="w")
            self.checkbuttons[category]=[checkbutton,CheckVar]
        
        self.goalscheckbutton_frames.grid(row=1,column=1)

        self.createsessionplan_button = ttk.Button(self.frame, text='Create Training Plan',command=lambda:self.create_sessionplan())
        self.createsessionplan_button.grid(row=2,column=1, padx=50, pady=15)



        