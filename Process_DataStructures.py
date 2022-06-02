import tkinter as tk
from tkinter import ttk
from datetime import datetime


import json


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
        def __init__(self,pandas_data,pandas_index, category_objects):

            self.ID = pandas_data.at[pandas_index, "ID"]
            self.descriptor = pandas_data.at[pandas_index,"Descriptor"]
            self.type = pandas_data.at[pandas_index,"Type"]
            
            # create a link with the CategoryData class based on the ID
            # stored in the exercisedata.csv file
            self.category = pandas_data.at[pandas_index,"Category"]
            self.categoryobj = category_objects[self.category]
            self.categoryobj.linkexercisedata(self)


    class CategoryData():
        """Holds attributes for a Category (e.g., upper body push). 
        The constructor requires:
        - Category pandas data structure
        - Index of the row which is being constructed"""
        def __init__(self,pandas_data, pandas_index):
            self.pandas_data=pandas_data
            self.pandas_index=pandas_index
            
            self.ID = self.pandas_data.at[self.pandas_index, "ID"]
            self.category = self.pandas_data.at[pandas_index,"Category"]
            self.exerciseobjects={}
        
        def linkexercisedata(self, exercise_data_object):
            """Adds a link to en ExerciseData object to this CategoryData object. 
            Note that [CategoryData] 1 -> 0..* [ExerciseData] meaning that every time
            an ExerciseData object is instantiated, this function will be called to
            add that exercise to the dictionary of exercises self.exerciseobjects()"""
            self.exerciseobjects[exercise_data_object.ID] = exercise_data_object

    def __init__(self):

        self.categoriesfile = pd.read_csv("categoriesdatabase.csv")
        self.categoriesfile = self.categoriesfile.fillna('')
        self.categoriesdata={} # dictionary used to store generated CategoryData objects
        # loop through all Categories and instantiate an object for each one
        i=0
        while i < len(self.categoriesfile):
            exercisedata_obj = self.CategoryData(self.categoriesfile, i)
            self.categoriesdata[exercisedata_obj.ID] = exercisedata_obj
            i += 1


        self.exercisefile = pd.read_csv("exercisedatabase.csv")
        self.exercisefile = self.exercisefile.fillna('')
        self.exercisedata={} # dictionary used to store generated objects

        # loop through rows in the file, and instantiate an 
        # ExerciseData object for each
        i=0
        while i < len(self.exercisefile):
            exercisedata_obj = self.ExerciseData(self.exercisefile,i, self.categoriesdata)
            # add object to the dictionary
            self.exercisedata[exercisedata_obj.ID]=exercisedata_obj
            i += 1
            





class CustomerData():
    
    class Trainee():
        """
            Initialise a Trainee object.
            - pandas_index = CSV row which is being read
            - pandas_data = entire pandas dataset of the CSV data
            - 
        """
        def __init__(self, pandas_data, pandas_index):
            
            self.pandas_index=pandas_index
            self.pandas_data=pandas_data

            self.ID = self.pandas_data.at[self.pandas_index, "ID"]
            self.name = self.pandas_data.at[self.pandas_index, "Name"]
            self.DoB = self.pandas_data.at[self.pandas_index, "DoB"]
            self.email = self.pandas_data.at[self.pandas_index, "Email"]

            self.ability_level = self.pandas_data.at[self.pandas_index, "AbilityLevel"]
            if str(self.ability_level) == "": self.ability_level = 1 # set default AbilityLevel if non-existent

            self.training_plans_string = self.pandas_data.at[self.pandas_index, "TrainingPlans"]
            # read the JSON (TrainingPlans) into a list-dictionary datastructure in Python
            if self.training_plans_string != "":self.training_plans = json.loads(self.training_plans_string)
            else: self.training_plans=[] # default to an empty list

            self.goals_string = self.pandas_data.at[self.pandas_index, "Goals"]
            # read the JSON (Goals) which are a currently a list representation in a string into a python list
            if self.goals_string != "":self.goals = json.loads(self.goals_string)
            else:self.goals=[] # default to an empty list

        def writetofile(self):
            #try:
            # insert all variables into the pandas object
            self.pandas_data.at[self.pandas_index,"Name"]=self.name
            self.pandas_data.at[self.pandas_index,"DoB"]=self.DoB
            self.pandas_data.at[self.pandas_index,"Email"]=self.email
            self.pandas_data.at[self.pandas_index,"Goals"]=str(self.goals)
            self.pandas_data.at[self.pandas_index,"AbilityLevel"]=str(self.ability_level)


            self.pandas_data.at[self.pandas_index,"TrainingPlans"]=json.dumps(self.training_plans)

            # write the object to a CSV
            self.pandas_data.to_csv("traineedata.csv", index=False)
            tk.messagebox.showinfo(message="Sucessfully made changes")
            #except Exception as e:
            #    tk.messagebox.showerror(message="Error(s) occured:\n\n" + str(e))


        def setDoB(self,new):
            self.DoB = new
        def getDoB(self):
            return self.DoB

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

    def __init__(self):
        self.cusomter_pd = pd.read_csv("traineedata.csv")
        self.cusomter_pd = self.cusomter_pd.fillna('') #replace empty fields (which would normally show NaN) with ""
        # format the Date of Birth as a date
        self.cusomter_pd['DoB'] = pd.to_datetime(self.cusomter_pd['DoB'], dayfirst=True, errors='coerce')

        self.traineedata = {}

        i=0
        # loop through each row/trainee in the datastructure
        while i < len(self.cusomter_pd):
            # create an object for each customer
            trainee_obj = self.Trainee(self.cusomter_pd, i)
            self.traineedata[trainee_obj.ID]=trainee_obj
            i = i + 1

