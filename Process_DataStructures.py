import datetime
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
            self.__controller=controller
            self.__pandas_index=pandas_index
            self.__category_objects=category_objects

        def load(self):

            self.__ID = str(int(self.__controller.exercisefile.at[self.__pandas_index, "ID"]))
            self.__descriptor = self.__controller.exercisefile.at[self.__pandas_index,"Descriptor"]
            self.__format = self.__controller.exercisefile.at[self.__pandas_index,"Format"]
            
            # create a link with the CategoryData class based on the ID
            # stored in the exercisedata.csv file
            self.__category = self.__controller.exercisefile.at[self.__pandas_index,"Category"]
            self.__categoryobj = self.__category_objects[self.__category]
            self.__categoryobj.linkexercisedata(self)


        @property
        def ID(self):
            return self.__ID

        @property
        def descriptor(self):
            return self.__descriptor

        @property
        def format(self):
            return self.__format

        @property
        def category(self):
            return self.__category


        def create_new(self,id,descriptor,format,categoryobj):
            self.__ID=id
            self.__descriptor=descriptor
            self.__format=format
            self.__categoryobj=categoryobj
            self.__category=categoryobj.ID

        def writetofile(self):
            #try:
            # insert all variables into the pandas object
            self.__controller.exercisefile.at[self.__pandas_index,"ID"]=self.__ID
            self.__controller.exercisefile.at[self.__pandas_index,"Descriptor"]=self.__descriptor
            self.__controller.exercisefile.at[self.__pandas_index,"Format"]=self.__format
            self.__controller.exercisefile.at[self.__pandas_index,"Category"]=self.__categoryobj.ID

            # write the object to a CSV
            try:
                self.__controller.exercisefile.to_csv("exercisedatabase.csv", index=False)
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
            self.__pandas_data=pandas_data
            self.__pandas_index=pandas_index
            self.__ID = self.__pandas_data.at[self.__pandas_index, "ID"]
            self.__category = self.__pandas_data.at[self.__pandas_index,"Category"]
            self.__exerciseobjects={}
        
        def linkexercisedata(self, exercise_data_object):
            """Method built into the CategoryData object. When an ExerciseData object is generated, it needs to be linked to it's respective CategoryData object (relationship in UML). This CategoryData object contains an array of ExerciseData objects which have a relationship with each category.
            This FUNCTION takes an exercise_data_object and adds it to the dictionary of objects within this CategoryData class."""
            self.__exerciseobjects[exercise_data_object.ID] = exercise_data_object

        @property
        def ID(self):
            return self.__ID

        @property
        def category(self):
            return self.__category

        @property
        def exerciseobjects(self):
            return self.__exerciseobjects


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
        """Injects data from the Pandas DataFrame into this Trainee object"""
        
        # initialise ID, name and DoB and email. These fields are all strings so can be directly brought over from the Pandas DataFrame
        self.__ID = self.__controller.cusomter_pd.at[self.__pandas_index, "ID"]
        self.__name = self.__controller.cusomter_pd.at[self.__pandas_index, "Name"]
        self.__DoB = self.__controller.cusomter_pd.at[self.__pandas_index, "DoB"]
        self.__email = self.__controller.cusomter_pd.at[self.__pandas_index, "Email"]
        
        # initialise the ability level, which must be converted to a float
        self.__ability_level = self.__controller.cusomter_pd.at[self.__pandas_index, "AbilityLevel"]
        if str(self.__ability_level) == "": self.__ability_level = 1 # set default AbilityLevel if non-existent
        
        # initialise the training plans for the Trainee. 
        # the following code will convert the string representation (JSON) of a TrainingPlan into a range of instantiated TrainingPlan objects
        self.__training_plans_string = self.__controller.cusomter_pd.at[self.__pandas_index, "TrainingPlans"]
        self.__training_plans = []
        # read the JSON (TrainingPlans) into a list-dictionary datastructure in Python
        if self.__training_plans_string != "":
            training_plans_with_string = json.loads(self.__training_plans_string)     
            for training_plan in training_plans_with_string:
                training_plan_obj = TrainingPlan(self.__mainline_obj, self)
                training_plan_obj.import_from_string(training_plan)
                self.__training_plans.append(training_plan_obj)
        
        # initialise the goals field. This needs to be converted from a string representatio of an array to an actual Python array
        self.__goals_string = self.__controller.cusomter_pd.at[self.__pandas_index, "Goals"]
        if self.__goals_string != "":self.__goals = json.loads(self.__goals_string)
        else:self.__goals=[] # default to an empty list

    def __init__(self, mainline_obj, controller, pandas_index): 
        """
        Constructs the Trainee class
        - mainline_obj: the object for the top level class which contains all the datastructures and top level GUI control
        - controller: the parent class (contains attributes like the Pandas DataFrame which need to be accessed within this function)
        - pandas_index: the row (index) of the Trainee being instantiated within this class (used when accesing Trainee from Pandas DataFrame)
        """  
        self.__mainline_obj=mainline_obj
        self.__pandas_index=pandas_index
        self.__controller=controller

    def create_trainee_object(self,id, name, email):
        """
        Injects the data for the Trainee into this object
        - id: the unique Trainee identifier
        - name: the name of the Trainee
        - email: the email of the Trainee
        """
        self.__ID=id
        self.__name=name
        self.__email=email
        self.__DoB=""
        self.__ability_level=1
        self.__training_plans=[]
        self.__goals=[]

        new_row_dataframe = {'ID':self.__ID,'Name': self.__name, 'DoB': self.__DoB, 'Email': self.__email, 'Goals':self.__goals, 'AbilityLevel':self.__ability_level}

        self.__controller.cusomter_pd = self.__controller.cusomter_pd.append(new_row_dataframe, ignore_index = True)
        self.__controller.cusomter_pd.to_csv("traineedata.csv", index=False)

    def writetofile(self, inhibit_success_msg=False):
        #try:
        # insert all variables into the pandas object
        self.__controller.cusomter_pd.at[self.__pandas_index,"Name"]=self.__name
        self.__controller.cusomter_pd.at[self.__pandas_index,"DoB"]=self.__DoB
        self.__controller.cusomter_pd.at[self.__pandas_index,"Email"]=self.__email
        self.__controller.cusomter_pd.at[self.__pandas_index,"Goals"]=str(self.__goals)
        self.__controller.cusomter_pd.at[self.__pandas_index,"AbilityLevel"]=str(self.__ability_level)

        training_plans_with_string = []
        for training_plan in self.__training_plans:
            training_plans_with_string.append(training_plan.export_to_string())

        self.__controller.cusomter_pd.at[self.__pandas_index,"TrainingPlans"]=json.dumps(training_plans_with_string)

        # write the object to a CSV
        try:
            self.__controller.cusomter_pd.to_csv("traineedata.csv", index=False)
        except PermissionError as e:
            tk.messagebox.showerror(message="Permission denied to save changes. Please make sure data files are not currently open on your desktop")
            return

            
        if not inhibit_success_msg:
            tk.messagebox.showinfo(message="Sucessfully made changes")

    # GETTERS AND SETTERS

    @property
    def ID(self):
        return self.__ID

    @property
    def name(self):
        return self.__name

    @property
    def email(self):
        return self.__email
    

    @property
    def ability_level(self):
        return self.__ability_level

    @property
    def training_plans(self):
        return self.__training_plans

    @property
    def goals(self):
        return self.__goals

    @property
    def DoB(self):
        return self.__DoB

    @DoB.setter
    def DoB(self, var):
        """
        Setter method for DoB (will check date format)
        """
        try:
            datetime.datetime.strptime(var, '%Y-%m-%d')
            self.__DoB=var
        except ValueError:
            raise ValueError("Incorrect data format, should be YYYY-MM-DD")
        

    @goals.setter
    def goals(self, var):
        """
        Setter method for goals
        """
        self.__goals=var

    @email.setter
    def email(self, var):
        """
        Setter method for email
        """
        self.__email=var

    @ability_level.setter
    def ability_level(self, var):
        """
        Setter method for ability_level
        """
        self.__ability_level=var



    def setAbilityLevel(self, var):
        try:
            float(var)
        except ValueError as e:
            raise e
        
        self.__ability_level = var

   
    def setEmail(self, var):
        self.__email = var
     

    def getAbilityLevel(self):
        return self.__ability_level

   
    def getEmail(self):
        return self.__email
     

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

