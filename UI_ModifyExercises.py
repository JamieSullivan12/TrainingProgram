import tkinter as tk
from tkinter import ttk
import random

import reuseable_dropdownpopup
from Process_ExercisesAPI import load_data
from General_bindframe import bindframe


class ModifyExercisesPage(ttk.Frame):


    class APIGeneratedExerciseRow(ttk.Frame):

        def __init__(self,mainline_obj, parent_frame, row_num, exercise):
            """
            Create a row of an exercise from the API
            - mainline_obj: the object of the top level mainline (used to access datastructures and top level frames)
            - parent_frame: the frame on which all ExerciseRows need to be placed
            - row_num: the row on which this ExerciseRow needs to go on
            - exercise: the exercise (string) for which the exercise row is to be created for 
            """

            self.mainline_obj = mainline_obj
            self.parent_frame = parent_frame
            self.exercise=exercise

            ttk.Frame.__init__(self, self.parent_frame)
            self.columnconfigure(0, weight=3)
            self.columnconfigure(1, weight=1)
            
            # horizontal line separating customer rows
            self.bottom_seperator = ttk.Separator(self,orient='horizontal')
            self.bottom_seperator.grid(row=2,column=0,columnspan=100,sticky="ew")

            # customer name and date of birth
            self.name_label = ttk.Label(self,text=exercise.name)
            self.name_label.grid(row=0, column=0, padx=(20,20),pady=20)
            
            self.grid(row=row_num,column=0,columnspan=100,sticky="ew",padx=40)
            
            # bind the double click action of this frame to the function new_exercise_click()
            # Note: bindframe is a general function stored in another file
            bindframe(self,"<Double-Button-1>",lambda e:self.new_exercise_click())



        def new_exercise_click(self):
            """
            Called when the user double clicks a row frome above. This function will initialise the process of adding the selected object to the dataset of exercises
            """

            # the user needs to be asked in a drop down, which category this belongs to
            # the following code will retrieve all the category names from the CategoryData object (in the mainline_obj).
            # it will then turn the aforementioned into a set which can be passed into the dropdownselector
            category_names = []
            for category in self.mainline_obj.categorydata_dict:
                category_names.append(self.mainline_obj.categorydata_dict[category].category)
            dropdown_choices = set(category_names)
            # creating the drop down menu for selecting a category. Note: this is a user defined function (see the function for more details)
            reuseable_dropdownpopup.dropdownselect(self.category_selection,f"Please select what category '{self.exercise.name}' fits in to", dropdown_choices)


        def category_selection(self, selection):
            """
            Called upon completion of the category dropdown (above)
            - selection: the selection from the previous dropdown (string) e.g., core/abs, upper body push etc.
            """
            self.selected_category_obj = None
            # find the respective CategoryData object for the selection made in the dropdown
            for category in self.mainline_obj.categorydata_dict:
                if self.mainline_obj.categorydata_dict[category].category == selection:
                    self.selected_category_obj = self.mainline_obj.categorydata_dict[category]
            
            # if the selected_category_obj was not found, then the user did not make a selection
            if self.selected_category_obj == None:
                tk.messagebox.showerror(message="Please make a selection")
                return

            # the user needs to be asked in a drop down, which format the exercise is (reps, distance, time ...)
            # the following code will retrieve all the types (defined in a dictionary in mainline_obj.types).
            # it will then turn the aforementioned into a set which can be passed into the dropdownselector
            type_names = []
            for type in self.mainline_obj.exercise_formats:
                type_names.append(self.mainline_obj.exercise_formats[type])
            dropdown_choices = set(type_names)
            # creating the drop down menu for selecting a format. Note: this is a user defined function (see the function for more details)
            reuseable_dropdownpopup.dropdownselect(self.type_selection,f"Please select what format '{self.exercise.name}' is", dropdown_choices)


        def type_selection(self, type_selection):
            """
            Called upon completion of the format dropdown (above)
            - selection: the selection from the previous dropdown (string) e.g., reps, distance, time ...
            """

            # find the respective format (type) from the dictionary in the mainline
            self.selected_format = None
            for type in self.mainline_obj.exercise_formats:
                if self.mainline_obj.exercise_formats[type] == type_selection:
                    self.selected_format = type
            
            # if the selected_format was not found, then the user did not make a selection
            if self.selected_format == None:
                tk.messagebox.showerror(message="Please make a selection")
                return

            # create a random five digit ID and ensure that there are no duplicates
            id = random.randint(99999,999999)
            while id in self.mainline_obj.exercisedata_dict:
                id = random.randint(99999,999999)
            
            ########### adding the exercise to permenant storage #########
            # NOTE: see the ExerciseData object for more information on the following processes
            exercise_index = self.mainline_obj.data_obj.get_current_exercise_index()
            self.mainline_obj.exercisedata_dict[id] = self.mainline_obj.data_obj.ExerciseData(self.mainline_obj.data_obj, exercise_index,self.mainline_obj.categorydata_dict)
            self.mainline_obj.exercisedata_dict[id].create_new(id,self.exercise.name,self.selected_format,self.selected_category_obj)
            self.mainline_obj.exercisedata_dict[id].writetofile()


    def RetrieveData(self):
        """
        Will retrieve the API data for the exercises from the Process_ExercisesAPI.py file
        """
        # empty any existing exercise rows and clear the textbox
        self.SearchFunction(clearsearchbox=True)

        # manage UI elements
        self.retrieve_online_button.grid_forget()
        self.loading_label = ttk.Label(self.add_exercise_online_frame, text="Loading excersises from online database. This may take a minute. Your window may stop responding after some time.")
        self.loading_label.grid(row=0,column=0,columnspan=2,sticky="w")
        self.add_exercise_online_frame.update()
        
        # load the API from Process_ExercisesAPI.py file
        self.API_exercise_objects = load_data()

        if len(self.API_exercise_objects)==0:tk.messagebox.showerror(message="An error occured contacting the servers. Please check your internet connection and try again.")
        else:
            tk.messagebox.showinfo(message=str(len(self.API_exercise_objects)) + " exercises loaded from the online database. Please enter a search request in the bar to continue. Type 'ALL' to see all exercises - WARNING: may have detrimental performance impacts.")
            self.listofrows=[]

            self.SearchFunction()
        self.loading_label.grid_forget()
        self.retrieve_online_button.grid(row=0,column=0,columnspan=2,sticky="ew")
 
    def SearchFunction(self, clearsearchbox = False):
        """
        Will search for a range of Exercise objects based on search parameters in the self.serch_textbox entry field
        - clearsearchbox (Bool): indicates whether the search box should be emptied in the process of searching. Default: False
        """
        if clearsearchbox: self.search_texbox.delete(0, 'end')

        search_filter = self.search_texbox.get()
        
        # remove all current rows printed on screen (they will be replaced)
        try:
            for row in self.listofrows:
                row.exercise_frame.grid_forget()
            self.listofrows=[]
        except Exception as e: 
            # exception will only occur if there are no rows
            self.listofrows=[]
        
        # managing UI search element
        if self.search_message.winfo_exists(): self.search_message.grid_forget()
        else: self.search_message = ttk.Label(self.add_exercise_online_frame, text="Please enter a search request above")

        if search_filter == "":
            # if filter empty - do not show any rows
            self.search_message.grid(row=2,column=0)
        else:
            row_num=3
            for exercise in self.API_exercise_objects:
                # create ApiGeneratedExerciseRow objects ONLY for those that match the search criteria
                if search_filter.lower()=="all" or search_filter.lower() in self.API_exercise_objects[exercise].name.lower():
                    self.listofrows.append(self.APIGeneratedExerciseRow(self.mainline_obj,self.add_exercise_online_frame,row_num,self.API_exercise_objects[exercise]))
                row_num+=1
            # if row_num has not changed - there has been no elements found
            if row_num == 3: tk.messagebox.showinfo(message="No results for '" + search_filter.lower() + "'")
        self.update()

        self.mainline_obj.scrollable_frame.update()

    def __init__(self, mainline_obj):
        # mainline_obj refers to the object in which the mainline algorithm occurs
        # this contains any crucial data that needs to be able to be accessed from anywhere within the program - like datastructures or the top level frame
        self.mainline_obj = mainline_obj

        # instantiate a new frame object (placing it on the top-level scrollable_frame and extend it to this class)
        ttk.Frame.__init__(self, self.mainline_obj.scrollable_frame)

        # widgets which are part of this page
        title = ttk.Label(self, text="Exercises")
        title.grid(row=0,column=0, padx=(20,10), pady=(10,0), sticky="w")

        self.add_exercise_manual_frame = ttk.LabelFrame(self,text="Manually Add Exercise")
        self.add_exercise_manual_frame.grid(row=1,column=0)

        self.add_exercise_online_frame = ttk.LabelFrame(self,text="Find Exercises Online")
        self.add_exercise_online_frame.grid(row=1,column=0, padx=20, pady=15)

        self.retrieve_online_button = ttk.Button(self.add_exercise_online_frame,text="Retrieve Data", command = self.RetrieveData)
        self.retrieve_online_button.grid(row=0,column=0,columnspan=2,sticky="ew")

        self.search_message = ttk.Label(self.add_exercise_online_frame, text="Please enter a search request above")
        self.search_texbox = ttk.Entry(self.add_exercise_online_frame, width=50)
        self.search_texbox.grid(row=1,column=0,padx=(10,0))
        self.search_button = ttk.Button(self.add_exercise_online_frame,text="Search", width=30,command=lambda:self.SearchFunction())
        self.search_button.grid(row=1,column=1, padx=(20,10),pady=10)