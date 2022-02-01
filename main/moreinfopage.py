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

    class SessionPlanRow():
        def see_session_details_clicked(self):
            self.controller.controller.frames["SessionPlanReviewPage"].injectdata(self.sessionplan_json, self.controller.customer)
            self.controller.controller.showwindow("SessionPlanReviewPage")

        def __init__(self,controller, sessionplan_json,row):
            self.sessionplan_json=sessionplan_json
            self.controller=controller
            self.row_container = ttk.Frame(self.controller.session_frame)

            self.heading=ttk.Label(self.row_container,text=f"Session Plan Generated: {sessionplan_json['timestamp']}")
            self.sesessiondetails_button = ttk.Button(self.row_container,text="See Session Details",command=self.see_session_details_clicked)
            self.sesessiondetails_button.grid(row=0,column=1,padx=30,pady=20)
            self.seperator = ttk.Separator(orient="horizontal")
            self.seperator.grid(row=1,column=0,sticky="ew")
            self.heading.grid(row=0,column=0,padx=20,pady=10,sticky="w")
            self.row_container.grid(row=row,column=0,stick="ew")



    def create_list_of_sessions(self):
        try: 
            self.session_frame.grid_forget()
            self.session_frame.destroy()
        except Exception as e:pass
        self.session_frame = ttk.LabelFrame(self.frame,text="Session Plans")
        self.session_frame.grid(row=3,column=0,columnspan=2)
        
        sessionplan_list=[]
        for session_plan in self.customer.session_plans:
            sessionplan_list.append(session_plan)
        
        sessionplan_rowobjects = []
        for row,session_plan in enumerate(sessionplan_list):
            sessionplan_row= self.SessionPlanRow(self,session_plan,row)
            sessionplan_rowobjects.append(sessionplan_row)

    def injectdata(self,customer):
        self.customer=customer
        self.title["text"]=f"Customer: {self.customer.name}"
        self.DoB_label["text"]=f"Date of Birth: {self.customer.DoB}"
        self.Email_Label["text"]=f"Email: {self.customer.email}"
        for checkbutton_id in self.checkbuttons:
            self.checkbuttons[checkbutton_id][1].set(0)
        for category in self.customer.categories:
            self.checkbuttons[category][1].set(1)
        
        self.create_list_of_sessions()




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
        self.controller.frames["SessionPlanReviewPage"].injectdata(sessioncreator_obj.sessionplan.trainingplanjson, self.customer)
        self.controller.showwindow("SessionPlanReviewPage")

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



        