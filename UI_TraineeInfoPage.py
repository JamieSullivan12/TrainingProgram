import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import Process_CreateTrainingPlan
import reuseable_datepopup
from General_bindframe import bindframe


class TraineeInfoPage(ttk.Frame):

    class SessionPlanRow(ttk.Frame):
        def see_session_details_clicked(self):
            """
            When a user requests to see more information about a training plan
            """
            self.page_controller.mainline_obj.frames["TrainingPlanReviewPage"].injectdata(self.training_plan, self.page_controller.customer)
            self.page_controller.mainline_obj.showwindow("TrainingPlanReviewPage")

        def __init__(self,page_controller, trainingplan_obj, row):
            """
            On this page, all historical training plans are shown in a column. Each training plan (row) widget is stored in this object.
            This class extends the tkinter Frame class as each training plan row IS a frame also. This class will then store any widgets attributed to said training plan within the extended Frame class.
            """
            # mainline_obj refers to the object in which the mainline algorithm occurs
            # this contains any crucial data that needs to be able to be accessed from anywhere within the program - like datastructures or the top level frame
            self.page_controller = page_controller
            self.trainingplan_obj = trainingplan_obj

            # instantiate a new frame object (placing it on the top-level scrollable_frame and extend it to this class)
            ttk.Frame.__init__(self, self.page_controller)

            # setting up the widgets of the row
            self.heading=ttk.Label(self,text=f"Training Plan Generated: {self.trainingplan_obj  .timestamp}")
            
            self.sesessiondetails_button = ttk.Button(self,text="See Details",command=self.see_session_details_clicked)
            self.sesessiondetails_button.grid(row=0,column=1,padx=30,pady=20)
            
            self.seperator = ttk.Separator(orient="horizontal")
            self.seperator.grid(row=1,column=0,sticky="ew")
            
            self.heading.grid(row=0,column=0,padx=20,pady=10,sticky="w")
            self.grid(row=row,column=0,stick="ew")

    def create_list_of_sessions(self):
        """
        Function populates the Session Plans frame with all historically generated plans of the trainee
        """
        try: 
            self.session_frame.grid_forget()
            self.session_frame.destroy()
        except Exception as e: pass

        # create the frame
        self.session_frame = ttk.LabelFrame(self,text="Session Plans")
        self.session_frame.grid(row=2,column=1,pady=20,sticky="nsew")
        
        # store all training plans for the Trainee in an array
        trainingplan_list=[]
        for training_plan in self.trainee.training_plans:
            trainingplan_list.append(training_plan)
        
        # create the UI objects for each Training Plan object stored in the array above
        sessionplan_rowobjects = []
        for row,training_plan in enumerate(trainingplan_list):
            sessionplan_row= self.SessionPlanRow(self,training_plan,row)
            sessionplan_rowobjects.append(sessionplan_row)

    def injectdata(self,trainee):
        """
        Function used to inject data about a specific trainee into the page objects. Called before the page is switched to.
        - trainee: TraineeData object for the trainee being shown on this page
        """
        self.trainee=trainee
       
        self.title["text"]=f"Trainee: {self.trainee.name}"
        self.DoB_label["text"]=f"Date of Birth: {self.trainee.DoB}"
        self.Email_Label["text"]=f"Email: {self.trainee.email}"
        self.AbilityLevel_Label["text"]=f"Ability Level: {self.trainee.ability_level}"
        for checkbutton_id in self.checkbuttons:
            self.checkbuttons[checkbutton_id][1].set(0)
        for goal in self.trainee.goals:
            self.checkbuttons[goal][1].set(1)
        
        self.create_list_of_sessions()

        bindframe(self.Email_Label,"<Double-Button-1>",lambda e:self.textchangerequest(self.customerinfo_frame,self.Email_Label,self.trainee.getEmail, self.trainee.setEmail, prefix="Email: "))
        bindframe(self.AbilityLevel_Label,"<Double-Button-1>",lambda e:self.textchangerequest(self.customerinfo_frame,self.AbilityLevel_Label,self.trainee.getAbilityLevel, self.trainee.setAbilityLevel, prefix="Ability Level: "))

        self.saveButton = ttk.Button(self.customerinfo_frame,text="Save Changes",command=self.trainee.writetofile)
        self.saveButton.grid(row=3,column=0, padx=10, pady=(0,15),columnspan=2,sticky="w")


    def create_trainingplan(self):
        """
        Function will initialise the training plan generation method
        """
        # create a new training plan obejct
        training_plan_obj = Process_CreateTrainingPlan.TrainingPlan(self.mainline_obj, self.trainee, self.planned_date)
        # call the method within that object to create the training plan
        training_plan_obj.generate_training_plan(number_of_circuits=self.number_of_circuits, number_of_supersets=self.number_of_supersets, number_of_sets=self.number_of_sets)
        # if an error occurs, then ignore the following
        if training_plan_obj.not_enough_exercises_error == False:
            # show the detailed page of the newly generated training plan
            self.mainline_obj.frames["TrainingPlanReviewPage"].injectdata(training_plan_obj, self.trainee)
            self.mainline_obj.showwindow("TrainingPlanReviewPage")

    def update_goals(self):
        goal_list = []
        for goal_id in self.checkbuttons:
            if self.checkbuttons[goal_id][1].get()==1:
                goal_list.append(goal_id)
        self.trainee.goals = goal_list
        self.trainee.writetofile(inhibit_success_msg=True)


    def changecircuitsvalue(self,*args):
        """
        Function which handles the scrollbar for the circuit selector changing
        - will update the text indicator next to the circuit scrollbar to show the value on which the slider is.
        """
        try:
            self.no_circuits_VALUE["text"] = int(self.no_circuits_SCALE.get())
            self.number_of_circuits = int(self.no_circuits_SCALE.get())
        except Exception as e: pass

    def changesupersetsvalue(self,*args):
        """
        Function which handles the scrollbar for the superset selector changing
        - will update the text indicator next to the supersets scrollbar to show the value on which the slider is.
        """
        try:
            self.no_supersets_VALUE["text"] = int(self.no_supersets_SCALE.get())
            self.number_of_supersets = int(self.no_supersets_SCALE.get())
        except Exception as e: pass

    def changesetsvalue(self,*args):
        """
        Function which handles the scrollbar for the set selector changing
        - will update the text indicator next to the sets scrollbar to show the value on which the slider is.
        """
        try:
            self.no_sets_VALUE["text"] = int(self.no_sets_SCALE.get())
            self.number_of_sets = int(self.no_sets_SCALE.get())
        except Exception as e: 
            pass

    def completeDoB_datechange(self,date):
        """
        When the user opts to change the date of birth of a trainee, this functionw will write that change to the TraineeData object
        """
        self.trainee.DoB = str(date)
        self.DoB_label["text"] = "Date of Birth: " + str(date)

    def textchangerequest(self,frame,label, getter, setter, prefix="", suffix=""):
        """
        Generalised code for a text field which can be edited (through a double click)
        - frame: the frame in which this event is occuring
        - label: the text (Label) field which needs to be made mofifiable
        - getter: a function which will return the current value for that field
        - setter: a function which will take (and apply) whatever the user has entered within the Entry box
        - prefix (OPTIONAL): when the user has finished entering the new value, it will be placed back into a text box - with a prefix if selected
        - suffix (OPTIONAL): when the user has finished entering the new value, it will be placed back into a text box - with a suffix if selected 
        """

        def cancel(label, entry, row, column, padx, pady, sticky):
            """
            Will destroy the entry box, and replace the label widget onto the screen (as it was initially)
            NOTE: this is called either when the user presses <Escape> or after the user presses <Enter> and the changes have been saved
            """
            entry.destroy()
            label.grid(row=row,column=column,sticky=sticky,padx=padx,pady=pady)
                    
        def apply(label, entry, row, column, padx, pady, sticky, prefix, suffix):
            """
            Will look at the Entry box for any changes, and write them to a desired lcoation (the setter method)
            """
            try:
                setter(entry.get())
            except Exception as e:
                messagebox.showerror(message="Unknown erro occured:\n\n" + str(e))
                cancel(label, entry, row, column, padx, pady, sticky)
                return
            
            # insert the newly entered value into the label widget which was grid forgot from the screen
            label["text"] = f"{prefix}{entry.get()}{suffix}"
            cancel(label, entry, row, column, padx, pady, sticky)
            
        # remember details of the current textbox (which will need to be removed for the Entry box)
        row    = label.grid_info()['row']
        column = label.grid_info()['column']
        padx = label.grid_info()['padx']
        pady = label.grid_info()['pady']
        sticky= label.grid_info()['sticky']
        # delete the label
        label.grid_forget()

        # create and place an Entry box into the location where the label was deleted
        current_value = getter()
        entry = ttk.Entry(frame)
        entry.grid(row=row,column=column,sticky=sticky,padx=padx,pady=pady)
        # pre-insert the value from the getter function
        entry.insert(tk.END, current_value)

        # bind return (save changes) and escape (cancel changes) keys
        entry.bind("<Return>",lambda e:apply(label, entry, row, column, padx, pady, sticky,prefix,suffix))
        entry.bind("<Escape>",lambda e:cancel(label, entry, row, column, padx, pady, sticky))
    

    def __init__(self, mainline_obj):
        # mainline_obj refers to the object in which the mainline algorithm occurs
        # this contains any crucial data that needs to be able to be accessed from anywhere within the program - like datastructures or the top level frame
        self.mainline_obj = mainline_obj

        # instantiate a new frame object (placing it on the top-level scrollable_frame and extend it to this class)
        ttk.Frame.__init__(self, self.mainline_obj.scrollable_frame)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # setting up widgets
        self.title = ttk.Label(self, text=f"Customer: ")
        self.title.grid(row=0,column=0, padx=20, pady=20, sticky="w")

        self.customerinfo_frame = ttk.LabelFrame(self, text="Customer Information")
        self.customerinfo_frame.grid(row=1,column=0,padx=20,pady=0,sticky="nsew")

        self.DoB_label = ttk.Label(self.customerinfo_frame, text=f"Date of Birth: ")
        self.DoB_label.grid(row=0,column=0, padx=10, pady=15, sticky="w")

        self.changeDoB_button = ttk.Button(self.customerinfo_frame, text="Change", command=lambda: reuseable_datepopup.dateselect("Select Date", self.completeDoB_datechange))
        self.changeDoB_button.grid(row=0,column=1)

        self.Email_Label = ttk.Label(self.customerinfo_frame, text=f"Email: ")
        self.Email_Label.grid(row=1,column=0, columnspan=2, padx=10, pady=15, sticky="w")

        self.AbilityLevel_Label = ttk.Label(self.customerinfo_frame)
        self.AbilityLevel_Label.grid(row=2,column=0,columnspan=2, padx=10,pady=15,sticky="w")

        self.goalscheckbutton_frames = ttk.LabelFrame(self, text="Customer Goals")
        self.goalscheckbutton_frames.grid(row=1,column=1, sticky="nsew")

        # setting up checkbox to see trainee goals
        self.checkbuttons={}
        for category in self.mainline_obj.categorydata_dict:
            CheckVar = tk.IntVar()
            checkbutton = ttk.Checkbutton(self.goalscheckbutton_frames,
                text=self.mainline_obj.categorydata_dict[category].category,
                variable=CheckVar,
                command=self.update_goals,
                onvalue=1,
                offvalue=0)
            checkbutton.pack(anchor="w")
            self.checkbuttons[category]=[checkbutton,CheckVar]
        



        self.create_training_plan_frame = ttk.LabelFrame(self, text="Create Training Plan")
        self.create_training_plan_frame.grid(row=2,column=0, padx=20, pady=20,sticky="ew")

        ### CREATING THE CREATE TRAINING PLAN WINDOW - has three scrollers:
        ### - Circuits: control the amount of circuits which will exist in the generated session
        ### - Supersets: control the number of supersets will exist in each circuit
        ### - Sets: control the number of sets will exist in each superset
  
        # creating the circuits label (appears to the left of the scale widget)
        self.no_circuits_LABEL = ttk.Label(self.create_training_plan_frame, text="Circuits")
        self.no_circuits_LABEL.grid(row=0,column=0,sticky="w",padx=(15,0))
        # creating the circuits scale widget (pre-setting the value to 2)
        self.no_circuits_SCALE = ttk.Scale(self.create_training_plan_frame, from_=1,to=6, command=self.changecircuitsvalue)
        self.no_circuits_SCALE.set(2)
        self.no_circuits_SCALE.grid(row=0,column=1,padx=(10,10),pady=10)
        # creating the circuits label indicating the current value of the scale widget
        self.no_circuits_VALUE = ttk.Label(self.create_training_plan_frame, text=int(self.no_circuits_SCALE.get()))
        self.no_circuits_VALUE.grid(row=0,column=2,sticky="w",padx=(0,15))
        self.number_of_circuits = int(self.no_circuits_SCALE.get())

        # creating a widget for the number of supersets (structure same as that for circuits)
        self.no_supersets_LABEL = ttk.Label(self.create_training_plan_frame, text="Supersets")
        self.no_supersets_LABEL.grid(row=1,column=0,sticky="w",padx=(15,0))
        self.no_supersets_SCALE = ttk.Scale(self.create_training_plan_frame, from_=2,to=8, command=self.changesupersetsvalue)
        self.no_supersets_SCALE.set(3)
        self.no_supersets_SCALE.grid(row=1,column=1,padx=(10,10),pady=10)
        self.no_supersets_VALUE = ttk.Label(self.create_training_plan_frame, text=int(self.no_supersets_SCALE.get()))
        self.no_supersets_VALUE.grid(row=1,column=2,sticky="w",padx=(0,15))
        self.number_of_supersets = int(self.no_supersets_SCALE.get())

        # creating a widget for the numebr of sets (structure same as that for circuits)
        self.no_sets_LABEL = ttk.Label(self.create_training_plan_frame, text="Sets")
        self.no_sets_LABEL.grid(row=2,column=0,sticky="w",padx=(15,0))
        self.no_sets_SCALE = ttk.Scale(self.create_training_plan_frame, from_=2,to=8,command=self.changesetsvalue)
        self.no_sets_SCALE.set(4)
        self.no_sets_SCALE.grid(row=2,column=1,padx=(10,10),pady=10)
        self.no_sets_VALUE = ttk.Label(self.create_training_plan_frame, text=int(self.no_sets_SCALE.get()))
        self.no_sets_VALUE.grid(row=2,column=2,sticky="w",padx=(0,15))
        self.number_of_sets = int(self.no_sets_SCALE.get())

        self.planned_date = None
        def dateselected(date):
            self.planned_date = date
            self.planned_date_label["text"] = "Selected Date: " + str(self.planned_date)

        self.choose_planned_date_button = ttk.Button(self.create_training_plan_frame, text="Plan a Date", command=lambda:reuseable_datepopup.dateselect("Select a date", dateselected))
        self.choose_planned_date_button.grid(row=3,column=0,columnspan=2,padx=15,pady=(15,5),sticky="w")

        self.planned_date_label = ttk.Label(self.create_training_plan_frame, text="No date selected")
        self.planned_date_label.grid(row=4,column=0,columnspan=2,padx=15, pady=(5,15), sticky="w")

        self.createsessionplan_button = ttk.Button(self.create_training_plan_frame, text='Create Training Plan',command=lambda:self.create_trainingplan())
        self.createsessionplan_button.grid(row=5,column=0, columnspan=2, padx=15, pady=(0,15), sticky="w")

