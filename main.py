import tkinter as tk
from tkinter import ttk
import sys, traceback

import UI_HomePage, UI_TraineePage, UI_AddTraineePage, UI_TraineeInfoPage, UI_TrainingPlanViewerPage, UI_ModifyExercises
import Process_DataStructures, scrollable_frame


class GUI():

    def setupmenubar(self):
        """ Configure the navigation bar (menubar) """
        
        # initialise menu bar object
        self.menubar = tk.Menu(self.toplevel_frame)

        # create the "Settings" menu
        self.optionsmenu = tk.Menu(self.menubar, tearoff=False)
        self.optionsmenu.add_command(label="Change Theme", command=lambda:self.change_theme())
        self.menubar.add_cascade(label="Settings", menu=self.optionsmenu)

        # create the "Navigate" menu
        self.navigate = tk.Menu(self.menubar, tearoff=False)
        self.navigate.add_command(label="Home", command=lambda:self.showwindow("HomePage"))
        self.navigate.add_command(label="Trainee Search", command=lambda:self.showwindow("CustomerPage"))
        self.navigate.add_command(label="Add Trainee", command=lambda:self.showwindow("AddTraineePage"))
        self.navigate.add_command(label="Add Exercise", command=lambda:self.showwindow("ModifyExercisesPage"))
        self.menubar.add_cascade(label="Navigate", menu=self.navigate)

        # place menu bar onto the toplevel_frame widget
        self.toplevel_frame.config(menu=self.menubar)

    def setupwindows(self):
        '''
        Initialise all GUI classes
        '''
        # when other GUI pages are initialised, they may begin trying to change the active page (using showwindow() method). this is prevented using the ignore_setup flag.
        self.ignore_setup=True 
        
        # store all GUI pages in a dictionary.
        self.frames={}

        # loop through all imported GUI objects (from other files)
        pages = [UI_HomePage.HomePage,UI_TraineePage.CustomerPage,UI_AddTraineePage.AddTraineePage, UI_TraineeInfoPage.TraineeInfoPage,UI_TrainingPlanViewerPage.TrainingPlanReviewPage, UI_ModifyExercises.ModifyExercisesPage]
        for page in pages:
            # if page already has been initalised, remove it
            if page.__name__ in self.frames:
                self.frames[page.__name__].grid_forget()
            # strore the name of the class (will be used as a key in the self.frames dict)
            page_name = page.__name__

            # initalise the GUI object. self is passed as the mainline_obj class. It allows all other GUI objects to access attributes and methods from this mainline class.
            frame = page(self)

            # for easy access, add the newly created object to a dictionary
            self.frames[page_name] = frame
           
        self.ignore_setup=False

    def resetwindows(self):
        """
        Reset the entire application - all windows will be removed, and then re-generated
        """
        # remove all windows
        for frame in self.frames:
            self.frames[frame].grid_forget()
        # regenerate all windows
        self.setupwindows()

    def showwindow(self, frame_name):
        '''
        Show a requested GUI class to the user.
        - frame_name is the name of that GUI class which needs to be shown
        '''
        # see setupwindows() method for description of self.ignore_setup
        if not self.ignore_setup:

            # remove ALL frames from the viewing window
            for frame in self.frames:
                self.frames[frame].grid_forget()
            
            # keep track of which frame is currently being shown to the user
            self.current_frame = frame_name
            self.current_frame_object = self.frames[frame_name]
            
            # place the requested frame on the window
            self.current_frame_object.grid(row=0,column=0)
            
            # update ALL widget elements
            self.scrollable_frame.update()

    def change_theme(self):
        '''
        Used to toggle between light mode and dark mode
        '''
        # NOTE: The theme's real name is sun-valley-<mode>
        if root.tk.call("ttk::style", "theme", "use") == "sun-valley-dark":
            # Set light theme
            root.tk.call("set_theme", "light")
        else:
            # Set dark theme
            root.tk.call("set_theme", "dark")

    def __init__(self,toplevel_frame):
        self.toplevel_frame=toplevel_frame

        ########### INITIALISING DATASTRUCTURES ############
        # initialising exercises data
        self.data_obj = Process_DataStructures.Data()
        self.exercisedata_dict = self.data_obj.exercisedata
        # initialising category data
        self.categorydata_dict = self.data_obj.categoriesdata
        # initialising customer data
        self.customerdata_obj = Process_DataStructures.CustomerData(self)
        self.customerdata_dict = self.customerdata_obj.traineedata
        # hard coding types of exercise codes. TODO: remove hard coding
        self.exercise_formats = {1:"reps",3:"time",5:"distance",6:"long distance"}

        ########### INITIALISING GUI ############
        # using developer-made generalised code to define a new frame with scrollbars
        self.scrollable_frame = scrollable_frame.ScrollableFrame(self.toplevel_frame)
        self.setupmenubar()
        self.setupwindows()
        self.showwindow("HomePage") # Show top the HomePage frame
   

def destroyer():
    """ Handle program exit - will close all windows and command lines to prevent the program from remaining open in the background"""
    root.quit()
    root.destroy()
    sys.exit()

# only run the following code if it has been initialised by the user
if __name__ == '__main__':
    # initialise tkinter window
    root = tk.Tk()
    root.withdraw()

    # initalising a parent TopLevel widget - is the top level frame which all other pages are placed on
    parent = tk.Toplevel(master=root)
    parent.grid_rowconfigure(0,weight=1)
    parent.grid_columnconfigure(0,weight=1)
    parent.title("Training App")
    parent.geometry('900x600')

    # setup UI styling
    parent.tk.call("source", "sun-valley.tcl")
    parent.tk.call("set_theme", "light")

    # handle program exit protocol
    root.protocol("WM_DELETE_WINDOW", destroyer)
    parent.protocol("WM_DELETE_WINDOW", destroyer)

    try:
        # initliase UI object (note GUI is a class above)
        gui = GUI(parent)
    except Exception as e:
        import datetime
        with open("log.txt","a") as f:
            f.write("\n\n\n\n####################")
            f.write(str(datetime.datetime.now()))
            f.write("####################\n\n")
            f.write(traceback.format_exc())
            
        tk.messagebox.showerror(message="An error ocurred. Please see details below. Note that a more detailed account can be found in log.txt within the source code directory:\n\n" + str(e))

    # continually loop to listen for event interrupts
    parent.mainloop()


