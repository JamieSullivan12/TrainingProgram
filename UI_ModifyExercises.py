
from doctest import master
from email import message
from encodings import search_function
import tkinter as tk
from tkinter import *
from tkinter import ttk
import main
import tkinter.messagebox
import pandas as pd
from datetime import datetime,date
import reuseable_dropdownpopup
from Process_ExercisesAPI import load_data
import random

class ModifyExercisesPage(ttk.Frame):


    class APIGeneratedExerciseRow():
        def bindframe(self,frame,sequence,func):
            frame.bind(sequence, func)
            for child in frame.winfo_children():
                child.bind(sequence, func)

        def __init__(self,master_controller, controller,row_num,exercise):
            self.exercise=exercise
            self.master_controller=master_controller
            self.controller=controller
            # creating child frame in which individual customer rows will appear
            self.exercise_frame = ttk.Frame(self.controller)
            self.exercise_frame.columnconfigure(0, weight=3)
            self.exercise_frame.columnconfigure(1, weight=1)
            # horizontal line separating customer rows
            self.bottom_seperator = ttk.Separator(self.exercise_frame,orient='horizontal')
            # customer name and date of birth
            self.name_label = ttk.Label(self.exercise_frame,text=exercise.name)
            self.name_label.grid(row=0, column=0, padx=(20,20),pady=20)
            
            self.bottom_seperator.grid(row=2,column=0,columnspan=100,sticky="ew")
            self.exercise_frame.grid(row=row_num,column=0,columnspan=100,sticky="ew",padx=40)
            self.bindframe(self.exercise_frame,"<Double-Button-1>",lambda e:self.new_exercise_click())

        def new_exercise_click(self):

            category_names = []
            for category in self.master_controller.categorydata_dict:
                category_names.append(self.master_controller.categorydata_dict[category].category)
            
            dropdown_choices = set(category_names)
            reuseable_dropdownpopup.dropdownselect(self.category_selection,f"Please select what category '{self.exercise.name}' fits in to", dropdown_choices)


        def category_selection(self, selection):
            self.selected_category_obj = ""
            for category in self.master_controller.categorydata_dict:
                if self.master_controller.categorydata_dict[category].category == selection:
                    self.selected_category_obj = self.master_controller.categorydata_dict[category]
            
            if selection == "Make a selection":
                tkinter.messagebox.showerror(message="Please make a selection")
                self.new_exercise_click()

            type_names = []
            for type in self.master_controller.types:
                type_names.append(self.master_controller.types[type])
            

            dropdown_choices = set(type_names)
            reuseable_dropdownpopup.dropdownselect(self.type_selection,f"Please select what format '{self.exercise.name}' is", dropdown_choices)


        def type_selection(self, type_selection):
            exercise_index = self.master_controller.data_obj.get_current_exercise_index()

            if type_selection == "Make a selection":
                tkinter.messagebox.showerror(message="Please make a selection")
                self.new_exercise_click()

            self.selected_type = ""
            for type in self.master_controller.types:
                if self.master_controller.types[type] == type_selection:
                    self.selected_type = type
            


            id = random.randint(0,999999)
            while id in self.master_controller.exercisedata_dict:
                id = random.randint(0,999999)
            
            self.master_controller.exercisedata_dict[id] = self.master_controller.data_obj.ExerciseData(self.master_controller.data_obj.exercisefile, exercise_index,self.master_controller.categorydata_dict)
            self.master_controller.exercisedata_dict[id].create_new(id,self.exercise.name,self.selected_type,self.selected_category_obj)

            self.master_controller.exercisedata_dict[id].writetofile()

    def save_changes(self, customers):
        '''
        FUNCTION: Save all changes the user has made in the customer table
        IN:
        - customers: A list of all the customer objects
        OUT:
        - None
        '''

        save_log = ""
        cancel = False

        for c in customers:
            if cancel==False: #break value
                # customer object method to check if changes have been made
                error_msg,items_changed=customers[c].check_difference()
                if error_msg!="":cancel=True # if an error occured when checking the differences, break out of the loop
                #if no errors occured, update all the values for that customer
                elif len(items_changed)>0 and error_msg=="":
                
                    self.controller.customer_df.at[customers[c].pandas_index,"Name"]=customers[c].name
                    self.controller.customer_df.at[customers[c].pandas_index,"DoB"]=customers[c].DoB
                    self.controller.customer_df.at[customers[c].pandas_index,"Goals"]=customers[c].goals
                    self.controller.customer_df.at[customers[c].pandas_index,"Email"]=customers[c].email
                    save_log+=f"Customer: {customers[c].name} updated.\n"

        if save_log=="" and error_msg=="":
            tkinter.messagebox.showinfo(title="No changes were made", message="No changes were made")
        elif save_log=="" and error_msg!="":
            tkinter.messagebox.showerror(title="An Error Occured!", message=error_msg)
        elif save_log!="":                
            self.controller.customer_df.to_csv("tempdata1.csv", index=False)
            try:
                self.controller.customer_df.to_csv("tempdata1.csv", index=False)
                tkinter.messagebox.showinfo(title="Successfully saved changes", message="Your changes were saved:\n\n" + save_log)
            except PermissionError as e:
                tkinter.messagebox.showerror(title="Unable to save changes", message="Please ensure that the core data file is not open and try again.")
    
    def set_heading(self):
        self.controller.tkRoot.title("Training App > Customers")

    def RetrieveData(self):
        self.SearchFunction(override=True)
        self.retrieve_online_button.grid_forget()
        self.loading_label = ttk.Label(self.add_exercise_online_frame, text="Loading excersises from online database. This may take a minute. Your window may stop responding after some time.")
        self.loading_label.grid(row=0,column=0,columnspan=2,sticky="w")
        self.add_exercise_online_frame.update()
        self.searchfilter_API = ""
        
        self.API_exercise_objects = load_data()

        if len(self.API_exercise_objects)==0:tkinter.messagebox.showerror(message="An error occured contacting the servers. Please check your internet connection and try again.")
        else:
            tkinter.messagebox.showinfo(message=str(len(self.API_exercise_objects)) + " exercises loaded from the online database. Please enter a search request in the bar to continue. Type 'ALL' to see all exercises - WARNING: may have detrimental performance impacts.")
            self.listofrows=[]

            self.SearchFunction()
        self.loading_label.grid_forget()
        self.retrieve_online_button.grid(row=0,column=0,columnspan=2,sticky="ew")
 
    def SearchFunction(self, override = False):
        if override:
            self.search_texbox.delete(0, 'end')
        search_filter = self.search_texbox.get()
        
        # remove all current customer rows printed on screen (they will be replaced)
        try:
            for row in self.listofrows:
                row.exercise_frame.grid_forget()
            self.listofrows=[]
        except Exception as e: listofrows=[]
        
        if self.search_message.winfo_exists(): 
            self.search_message.grid_forget()
        else:
            self.search_message = ttk.Label(self.add_exercise_online_frame, text="Please enter a search request above")

        if search_filter == "":
            self.search_message.grid(row=2,column=0)
        else:
            row_num=3
            for exercise in self.API_exercise_objects:
                
                if search_filter.lower()=="all" or search_filter.lower() in self.API_exercise_objects[exercise].name.lower():
                    self.listofrows.append(self.APIGeneratedExerciseRow(self.controller,self.add_exercise_online_frame,row_num,self.API_exercise_objects[exercise]))
                row_num+=1
            if row_num == 3: tkinter.messagebox.showinfo(message="No results for '" + search_filter.lower() + "'")
        self.update()

        self.controller.frame_obj.update()

    def __init__(self, controller):
        ttk.Frame.__init__(self, controller.frame_obj.scrollable_frame)
        self.controller = controller

        title = ttk.Label(self, text="Exercises")
        title.grid(row=0,column=0, padx=(20,10), pady=(10,0), sticky="w")

        self.add_exercise_manual_frame = ttk.LabelFrame(self,text="Manually Add Exercise")

        self.add_exercise_manual_frame.grid(row=1,column=0)

        self.add_exercise_online_frame = ttk.LabelFrame(self,text="Find Exercises Online")
        self.retrieve_online_button = ttk.Button(self.add_exercise_online_frame,text="Retrieve Data", command = self.RetrieveData)
        self.retrieve_online_button.grid(row=0,column=0,columnspan=2,sticky="ew")

        self.add_exercise_online_frame.grid(row=1,column=0, padx=20, pady=15)

        self.search_message = ttk.Label(self.add_exercise_online_frame, text="Please enter a search request above")
        self.search_texbox = ttk.Entry(self.add_exercise_online_frame, width=50)
        self.search_texbox.grid(row=1,column=0,padx=(10,0))
        self.search_button = ttk.Button(self.add_exercise_online_frame,text="Search", width=30,command=lambda:self.SearchFunction())
        self.search_button.grid(row=1,column=1, padx=(20,10),pady=10)