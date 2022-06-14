from doctest import master
import tkinter as tk
import json
from Process_CreateTrainingPlan import TrainingPlan


import pandas as pd

class Data():
    
    class ExerciseData():
        """
        Holds attributes for an Exercise (e.g., pushups). 
        The constructor requires:
        - Exercise pandas data structure
        - Index of the row which is being constructed
        - Dictionary of category objects (for relationship linking purposes).
                Note that the dictionary will be {CategoryData ID: CategoryData object}
        """
        def __init__(self,controller,pandas_index,category_objects):
            self.controller=controller
            self.pandas_index=pandas_index
            self.category_objects=category_objects
        
        def load(self):

            self.ID = str(int(self.controller.exercisefile.at[self.pandas_index, "ID"]))
            self.descriptor = self.controller.exercisefile.at[self.pandas_index,"Descriptor"]
            self.type = self.controller.exercisefile.at[self.pandas_index,"Type"]
            
            # create a link with the CategoryData class based on the ID
            # stored in the exercisedata.csv file
            self.category = self.controller.exercisefile.at[self.pandas_index,"Category"]
            self.categoryobj = self.category_objects[self.category]
            self.categoryobj.linkexercisedata(self)

        def create_new(self,id,descriptor,type,categoryobj):
            self.ID=id
            self.descriptor=descriptor
            self.type=type
            self.categoryobj=categoryobj
            self.category=categoryobj.ID

        def writetofile(self):
            #try:
            # insert all variables into the pandas object
            self.controller.exercisefile.at[self.pandas_index,"ID"]=self.ID
            self.controller.exercisefile.at[self.pandas_index,"Descriptor"]=self.descriptor
            self.controller.exercisefile.at[self.pandas_index,"Type"]=self.type
            self.controller.exercisefile.at[self.pandas_index,"Category"]=self.categoryobj.ID

            # write the object to a CSV
            try:
                self.controller.exercisefile.to_csv("exercisedatabase.csv", index=False)
            except PermissionError as e:
                tk.messagebox.showerror(message="Permission denied to save changes. Please make sure data files are not currently open on your desktop")
                return

            tk.messagebox.showinfo(message="Sucessfully made changes")


    class CategoryData():
        """Holds attributes for a Category (e.g., upper body push). 
        The constructor requires:
        - pandas_data: pandas data structure with raw data
        - Index of the row/category which is being constructed in this object"""
        def __init__(self,pandas_data, pandas_index):
            self.pandas_data=pandas_data
            self.pandas_index=pandas_index
            self.ID = self.pandas_data.at[self.pandas_index, "ID"]
            self.category = self.pandas_data.at[pandas_index,"Category"]
            self.exerciseobjects={}
        
        def linkexercisedata(self, exercise_data_object):
            """Method built into the CategoryData object. When an ExerciseData object is generated, it needs to be linked to it's respective CategoryData object (relationship in UML). This CategoryData object contains an array of ExerciseData objects which have a relationship with each category.
            This FUNCTION takes an exercise_data_object and adds it to the dictionary of objects within this CategoryData class."""
            self.exerciseobjects[exercise_data_object.ID] = exercise_data_object

    def __init__(self):
        self.categoriesfile = pd.read_csv("categoriesdatabase.csv")
        self.categoriesfile = self.categoriesfile.fillna('')
        self.categoriesdata={} # dictionary used to store generated CategoryData objects
        # loop through all Categories and instantiate an object for each one
        i=0
        while i < len(self.categoriesfile):
            categorydata_obj = self.CategoryData(self.categoriesfile, i)
            self.categoriesdata[categorydata_obj.ID] = categorydata_obj
            i += 1

        self.exercisefile = pd.read_csv("exercisedatabase.csv")
        self.exercisefile = self.exercisefile.fillna('')
        self.exercisedata={} # dictionary used to store generated objects

        # loop through rows in the file, and instantiate an 
        # ExerciseData object for each
        self.exercise_index=0
        while self.exercise_index < len(self.exercisefile):
            exercisedata_obj = self.ExerciseData(self,self.exercise_index, self.categoriesdata)
            # add object to the dictionary
            exercisedata_obj.load()
            self.exercisedata[exercisedata_obj.ID]=exercisedata_obj
            self.exercise_index += 1
    
    def get_current_exercise_index(self):
        self.exercise_index += 1
        return (self.exercise_index-1)
        


class Trainee():

    def read_trainee_object(self):
        """
        Injects data from the Pandas DataFrame into this Trainee object
        """
        # initialise ID, name and DoB and email. These fields are all strings so can be directly brought over from the Pandas DataFrame
        self.ID = self.controller.cusomter_pd.at[self.pandas_index, "ID"]
        self.name = self.controller.cusomter_pd.at[self.pandas_index, "Name"]
        self.DoB = self.controller.cusomter_pd.at[self.pandas_index, "DoB"]
        self.email = self.controller.cusomter_pd.at[self.pandas_index, "Email"]
        
        # initialise the ability level, which must be converted to a float
        self.ability_level = self.controller.cusomter_pd.at[self.pandas_index, "AbilityLevel"]
        if str(self.ability_level) == "": self.ability_level = 1 # set default AbilityLevel if non-existent
        
        # initialise the training plans for the Trainee. 
        # the following code will convert the string representation (JSON) of a TrainingPlan into a range of TrainingPlan objects which will be instantiated
        self.training_plans_string = self.controller.cusomter_pd.at[self.pandas_index, "TrainingPlans"]
        self.training_plans = []
        # read the JSON (TrainingPlans) into a list-dictionary datastructure in Python
        if self.training_plans_string != "":
            training_plans_with_string = json.loads(self.training_plans_string)     
            for training_plan in training_plans_with_string:
                training_plan_obj = TrainingPlan(self.mainline_obj, self)
                training_plan_obj.import_from_string(training_plan)
                self.training_plans.append(training_plan_obj)
        
        # initialise the goals field. This needs to be converted from a string representatio of an array to an actual Python array
        self.goals_string = self.controller.cusomter_pd.at[self.pandas_index, "Goals"]
        if self.goals_string != "":self.goals = json.loads(self.goals_string)
        else:self.goals=[] # default to an empty list

    def __init__(self, mainline_obj, controller, pandas_index): 
        """
        Constructs the Trainee class
        - mainline_obj: the object for the top level class which contains all the datastructures and top level GUI control
        - controller: the parent class (contains attributes like the Pandas DataFrame which need to be accessed within this function)
        - pandas_index: the row (index) of the Trainee being instantiated within this class (used when accesing Trainee from Pandas DataFrame)
        """  
        self.mainline_obj=mainline_obj
        self.pandas_index=pandas_index
        self.controller=controller

    def create_trainee_object(self,id, name, email):
        """
        Injects the data for the Trainee into this object
        - id: the unique Trainee identifier
        - name: the name of the Trainee
        - email: the email of the Trainee
        """
        self.ID=id
        self.name=name
        self.email=email
        self.DoB=""
        self.ability_level=1
        self.training_plans=[]
        self.goals=[]

        new_row_dataframe = {'ID':self.ID,'Name': self.name, 'DoB': self.DoB, 'Email': self.email, 'Goals':self.goals, 'AbilityLevel':self.ability_level}

        self.controller.cusomter_pd = self.controller.cusomter_pd.append(new_row_dataframe, ignore_index = True)
        self.controller.cusomter_pd.to_csv("traineedata.csv", index=False)

    def writetofile(self, inhibit_success_msg=False):
        #try:
        # insert all variables into the pandas object
        self.controller.cusomter_pd.at[self.pandas_index,"Name"]=self.name
        self.controller.cusomter_pd.at[self.pandas_index,"DoB"]=self.DoB
        self.controller.cusomter_pd.at[self.pandas_index,"Email"]=self.email
        self.controller.cusomter_pd.at[self.pandas_index,"Goals"]=str(self.goals)
        self.controller.cusomter_pd.at[self.pandas_index,"AbilityLevel"]=str(self.ability_level)

        training_plans_with_string = []
        for training_plan in self.training_plans:
            training_plans_with_string.append(training_plan.export_to_string())

        self.controller.cusomter_pd.at[self.pandas_index,"TrainingPlans"]=json.dumps(training_plans_with_string)

        # write the object to a CSV
        try:
            self.controller.cusomter_pd.to_csv("traineedata.csv", index=False)
        except PermissionError as e:
            tk.messagebox.showerror(message="Permission denied to save changes. Please make sure data files are not currently open on your desktop")
            return

            
        if not inhibit_success_msg:
            tk.messagebox.showinfo(message="Sucessfully made changes")



    def setDoB(self,new):
        self.DoB = new
    def getDoB(self):
        return str(self.DoB)

    def setEmail(self,new):
        self.email = new
    def getEmail(self):
        return self.email

    def setAbilityLevel(self,new):
        self.ability_level = float(new)
    def getAbilityLevel(self):
        return self.ability_level

    def removesessionplan(self,session_plan):
        for plan in self.training_plans:
            if plan["timestamp"] == session_plan["timestamp"]:
                self.training_plans.remove(plan)


def format_date(date):
    return pd.to_datetime(date).apply(lambda x: x.strftime('%d/%m/%Y')if not pd.isnull(x) else '')

class CustomerData():
    
    def __init__(self, mainline_obj):
        self.cusomter_pd = pd.read_csv("traineedata.csv")
        self.cusomter_pd = self.cusomter_pd.fillna('')
        self.traineedata = {}

        self.i=0
        # loop through each row/trainee in the datastructure
        while self.i < len(self.cusomter_pd):
            # create an object for each Trainee
            trainee_obj = Trainee(mainline_obj, self, self.i)
            trainee_obj.read_trainee_object()
            self.traineedata[trainee_obj.ID]=trainee_obj
            self.i = self.i + 1
    

    def get_current_index(self):
        self.i = self.i + 1
        return (self.i - 1)

