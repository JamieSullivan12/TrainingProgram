import tkinter as tk
from tkinter import ttk
from General_bindframe import bindframe

'''
Contains the code for the customer page. On this page, the user can access all customer details and change them
'''
class CustomerPage(ttk.Frame):

    class TraineeRow(ttk.Frame): 
        
        def trainee_click(self):
            """
            Go to the TraineeInfoPage for the "clicked" trainee
            - Injects data for this customer object into the TraineeInfoPage (using abstracted function .injectdata). 
            - Then switches to that page using the showwindow function from the mainline object
            """
            self.page_object.mainline_obj.frames["TraineeInfoPage"].injectdata(self.customer)
            self.page_object.mainline_obj.showwindow("TraineeInfoPage")


        def __init__(self,page_object,row_num,customer):
            """
            UI object that will create a row (to be shown under the search bar) for each customer in the database.
            IN:
            - page_object: top level object for this page
            - row_num: the row on which this object needs to be placed
            - customer: the trainee for who to make this row
            """
            # create a row for this specified customer
            self.customer=customer

            # page_object refers to the top-level object for this page
            # this contains any crucial data that needs to be able to be accessed from anywhere within the program - like datastructures or the top level frame
            self.page_object = page_object

            # instantiate a new frame object (placing it on the top-level scrollable_frame and extend it to this class)
            ttk.Frame.__init__(self, self.page_object)
            self.columnconfigure(0, weight=3)
            self.columnconfigure(1, weight=1)
            
            # horizontal line separating customer rows
            self.bottom_seperator = ttk.Separator(self,orient='horizontal')
            self.bottom_seperator.grid(row=2,column=0,columnspan=100,sticky="ew")

            # trainee name and date of birth widgets (values taken from the customer object)
            self.name_label = ttk.Label(self,text=customer.name)
            self.name_label.grid(row=0, column=0, padx=(20,60),pady=20)
            self.email_label = ttk.Label(self, text=f"{customer.email}")
            self.email_label.grid(row=0, column=1)

            # place this frame on the specified row/column
            self.grid(row=row_num,column=0,columnspan=100,sticky="ew",padx=40)

            # bind the double click action on this frame to the trainee_click function
            # note the bindframe function is developer-defined in a seperate python file (imported above)
            bindframe(self,"<Double-Button-1>",lambda e: self.trainee_click())


    def searchfunction(self):
        """
        Prints all Trainees in the database. Will only include what is in the searchbox (defined in class initialisation).
        This function should be called every time the search button on the UI is pressed
        NOTE: if searchbox is empty, the filter will include all Trainees
        NOTE: this function will use the TraineeRows class for each trainee
        """
        # get the search parameter
        search_filter = self.search_texbox.get()

        # remove all current Trainee rows on screen (they will be replaced during the search algorithm)
        for row in self.listofrows:
            row.customer_frame.grid_forget()
        self.listofrows=[]
        
        row_num=2 # value which records the row on which each Trainee is printed on the UI. Starts on 2 to avoid the already-placed elements on the GUI
        
        # for each customer in the dataset, if it satisfies the search requirements, initialise and append the new customer row to a list
        for customer in self.mainline_obj.customerdata_dict:
            # non-case-senitive search
            if search_filter=="" or search_filter.lower() in self.mainline_obj.customerdata_dict[customer].name.lower() or search_filter.lower() in self.mainline_obj.customerdata_dict[customer].email.lower():
                self.listofrows.append(self.TraineeRow(self,row_num,self.mainline_obj.customerdata_dict[customer]))
                row_num+=1



    def __init__(self, mainline_obj):
        # mainline_obj refers to the object in which the mainline algorithm occurs
        # this contains any crucial data that needs to be able to be accessed from anywhere within the program - like datastructures or the top level frame
        self.mainline_obj = mainline_obj

        # instantiate a new frame object (placing it on the top-level scrollable_frame and extend it to this class)
        ttk.Frame.__init__(self, self.mainline_obj.scrollable_frame)

        # initialise widgets
        title = ttk.Label(self, text="Trainee Search")
        title.grid(row=0,column=0, padx=(40,10), pady=(10,0), sticky="w")

        self.search_texbox = ttk.Entry(self, width=50)
        self.search_texbox.grid(row=1,column=0,padx=(40,0))
        self.search_button = ttk.Button(self,text="Search", width=30,command=lambda:self.searchfunction())
        self.search_button.grid(row=1,column=1, padx=(20,10),pady=10)

        # searchfunction will load all of the trainees onto the page
        # listofrows will store all of these (accessed from within the search function)
        self.listofrows=[]
        self.searchfunction()