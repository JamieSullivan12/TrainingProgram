import tkinter as tk
from tkinter import ttk
import UI_HomePage, UI_TraineePage, UI_AddCustomerpage, UI_TraineeInfoPage, UI_TrainingPlanViewerPage, UI_ModifyExercises
import pandas as pd
import Process_DataStructures

class Tracker:
    """ Toplevel windows resize event tracker. """

    def __init__(self, toplevel):
        self.toplevel = toplevel
        self.width, self.height = toplevel.winfo_width(), toplevel.winfo_height()
        self._func_id = None

    def bind_config(self):
        self._func_id = self.toplevel.bind("<Configure>", self.resize)
        
    def unbind_config(self):  # Untested.
        if self._func_id:
            self.toplevel.unbind("<Configure>", self._func_id)
            self._func_id = None

    def resize(self, event):
        if(event.widget == self.toplevel and
           (self.width != event.width or self.height != event.height)):
            self.width, self.height = event.width, event.height
            if hasattr(self,"scrollable_frame"):
                self.scrollable_frame.update()
        
    def link_scrollable_frame(self,scrollable_frame):
        self.scrollable_frame = scrollable_frame



class GUI(ttk.Frame):
    def __init__(self,parent,tracker):
        self.parent=parent
        self.tracker=tracker

        # setup parent container and child frame which is horizontally and vertically scrollable
        self.container = ttk.Frame(self.parent)
        self.container.grid_rowconfigure(0,weight=1)
        self.container.grid_columnconfigure(0,weight=1)
        self.frame_obj = self.CreateScrollableFrame(self)
        # function that tracks ALL clicks on the Tkinter window
        self.tracker.link_scrollable_frame(self.frame_obj)


        # initialising exercises data
        self.data_obj = Process_DataStructures.Data()
        self.exercisedata_dict = self.data_obj.exercisedata
        # initialising category data
        self.categorydata_dict = self.data_obj.categoriesdata
        # initialising customer data
        self.customerdata_obj = Process_DataStructures.CustomerData(self)
        self.customerdata_dict = self.customerdata_obj.traineedata

        # create all pages that the user can navigate to
        self.setupwindows()
        # only show the home page (initial page the user is greeted with)
        self.showwindow("HomePage")

        # configure the navigation menu/bar
        self.menubar = tk.Menu(self.parent)
        self.optionsmenu = tk.Menu(self.menubar, tearoff=False)
        self.optionsmenu.add_command(label="Change Theme", command=lambda:self.change_theme())
        self.menubar.add_cascade(label="Settings", menu=self.optionsmenu)
        self.navigate = tk.Menu(self.menubar, tearoff=False)
        self.navigate.add_command(label="Home", command=lambda:self.showwindow("HomePage"))
        self.navigate.add_command(label="Customer Page", command=lambda:self.showwindow("CustomerPage"))
        self.menubar.add_cascade(label="Navigate", menu=self.navigate)
        self.parent.config(menu=self.menubar)
        


        self.container.pack(side='top', fill='both', expand=True)
    '''
    Used to toggle between light mode and dark mode
    '''
    def change_theme(self):
        # NOTE: The theme's real name is sun-valley-<mode>
        if root.tk.call("ttk::style", "theme", "use") == "sun-valley-dark":
            # Set light theme
            root.tk.call("set_theme", "light")
        else:
            # Set dark theme
            root.tk.call("set_theme", "dark")

    
    '''
    Initialise all GUI classes
    '''
    def setupwindows(self):
        # when other GUI pages are initialised, they may begin trying to change the active page (using showwindow() method). this is prevented using the ignore_setup flag.
        self.ignore_setup=True 
        
        # store all created frames (top level containers) in a dictionary.
        # used when the user switches pages (requested frame brought to front)
        self.frames={}

        # loop through all imported GUI objects (from other files)
        pages = [UI_HomePage.HomePage,UI_TraineePage.CustomerPage,UI_AddCustomerpage.AddCustomerPage, UI_TraineeInfoPage.MoreInfoPage,UI_TrainingPlanViewerPage.SessionPlanReviewPage, UI_ModifyExercises.ModifyExercisesPage]
        for page in pages:
            # if page already has been initalised, remove it
            if page.__name__ in self.frames:
                self.frames[page.__name__].grid_forget()
            page_name = page.__name__

            # initalise the GUI object. self is passed as a "parent class"
            frame = page(self)

            # keep track of the initialised pages in a dict {page name: frame}
            self.frames[page_name] = frame
           
        self.ignore_setup=False


    '''
    Will place a requested frame (passed as an argument) on the user's viewing window
    - Note that all GUI objects must inherit the ttk.Frame class for this to work
    '''
    def showwindow(self, frame_name):
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
            self.frame_obj.update()




    class CreateScrollableFrame(ttk.Frame):
        '''
        Class to create a frame which can be scrolled through (complicated structure using a tkinter canvas widget).
        '''
        def __init__(self,parent):
            self.parent=parent

            # inherit all attributes & methods from the ttk.Frame widget
            super().__init__(self.parent.container)
            
            # create the canvas, vertical and horizontal scrollbar
            self.scrollable_canvas = tk.Canvas(parent.container, bd=0, highlightthickness=0)
            self.scrollbar = ttk.Scrollbar(self.parent.container, orient="vertical", command=self.scrollable_canvas.yview)
            self.hscrollbar = ttk.Scrollbar(self.parent.container, orient="horizontal", command=self.scrollable_canvas.xview)
            self.scrollable_frame = ttk.Frame(self.scrollable_canvas)
            # place the frmae on the canvas
            self.scrollable_canvas.create_window((0,0), window=self.scrollable_frame, anchor='nw')
            # setup the scrolling actions
            self.bind("<Configure>", lambda e: self.scrollable_canvas.configure(scrollregion = self.scrollable_canvas.bbox("all")))
            self.scrollable_canvas.configure(yscrollcommand=self.scrollbar.set)
            self.scrollable_canvas.configure(xscrollcommand=self.hscrollbar.set)
            self.hscrollbar.grid(row=1, column=0, sticky="ew")
            self.scrollbar.grid(row=0, column=1, sticky="ns")
            self.scrollable_canvas.grid(row=0, column=0, sticky="nsew")
            # bind mousewheel to scrolling action
            self.bind_all("<MouseWheel>", self._on_mousewheel)
            
            self.update()

        '''
        Link scrolling of the mouse wheel to the scrollbar
        - _bound_to_mousewheel: called whenever the pointer enters the canvas
        - _unbound_to_mousewheel: called whenever the pointer leaves the canvas
        - _on_mousewheel: called whenever the mousewheel scroll is detected (unless pointer is 
            outside of canvas)
        '''
        def _bound_to_mousewheel(self, event):
            self.scrollable_canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        def _unbound_to_mousewheel(self, event):   
            self.scrollable_canvas.unbind_all("<MouseWheel>")
        def _on_mousewheel(self, event):
            if self.vscrollable:
                self.scrollable_canvas.yview_scroll(int(-1*(event.delta/120)), "units")


        def update(self):
            """
            Update the scrollwheels on the scrollable frame to match contents
            """
            self.parent.parent.update_idletasks()
            if self.parent.container.winfo_height() >= self.scrollable_frame.winfo_height()+20:
                self.vscrollable=False
            else:
                self.vscrollable=True

            self.scrollable_canvas.update_idletasks()
            self.scrollable_canvas.config(scrollregion=self.scrollable_frame.bbox())
            

# only run the following code if it has been initialised by the user
if __name__ == '__main__':
    # initialise tkinter object
    root = tk.Tk()
    root.withdraw()
    parent = tk.Toplevel(master=root)
    root.title("Training App")
    tracker = Tracker(parent)
    tracker.bind_config()
    # setup UI styling
    parent.tk.call("source", "sun-valley.tcl")
    parent.tk.call("set_theme", "light")

    # initliase UI object (note GUI is a class above)
    gui = GUI(parent,tracker)

    # continually loop to listen for events
    parent.mainloop()

    