import tkinter as tk
from tkinter import ttk
import homepage, customerpage, addcustomerpage, moreinfopage, sessionplanreview
import pandas as pd
import datastructures

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
        self.container = ttk.Frame(self.parent)

        self.container.grid_rowconfigure(0,weight=1)
        self.container.grid_columnconfigure(0,weight=1)
        # create datastructure from raw data using pandas

        self.customerdata_obj = datastructures.CustomerData()
        self.customerdata_dict = self.customerdata_obj.customerdata

        self.data_obj = datastructures.ExerciseData()
        self.exercisedata_dict = self.data_obj.exercisedata

        self.categorydata_dict = self.data_obj.categoriesdata

        self.frame_obj = self.CreateScrollableFrame(self)
        self.tracker.link_scrollable_frame(self.frame_obj)

        #configuring the menu
        self.menubar = tk.Menu(self.parent)
        self.optionsmenu = tk.Menu(self.menubar, tearoff=False)
        self.optionsmenu.add_command(label="Change Theme", command=lambda:self.change_theme())
        self.menubar.add_cascade(label="Settings", menu=self.optionsmenu)
        self.navigate = tk.Menu(self.menubar, tearoff=False)
        self.navigate.add_command(label="Home", command=lambda:self.showwindow("HomePage"))
        self.navigate.add_command(label="Customer Page", command=lambda:self.showwindow("CustomerPage"))
        self.menubar.add_cascade(label="Navigate", menu=self.navigate)
        self.parent.config(menu=self.menubar)
        
        self.setupwindows()
        self.showwindow("HomePage")




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
    Initialises all other GUI classes, creating all the required windows and stacking them inside the container
    '''
    def setupwindows(self):
        # calling on other page classes means commands will be pre-loaded== that are not available yet (such as page loading)
        # ignore_setup will make sure these effects are not run
        self.ignore_setup=True 
        #
        self.frames={}
        pages = [homepage.HomePage,customerpage.CustomerPage,addcustomerpage.AddCustomerPage, moreinfopage.MoreInfoPage,sessionplanreview.SessionPlanReviewPage]


        # setup all page classes
        for page in pages:
            if page.__name__ in self.frames:
                self.frames[page.__name__].grid_forget()
            page_name = page.__name__
            frame = page(self) # initialise class
            self.frames[page_name] = frame # store list of classes (UI pages) in a list
        
           
        self.ignore_setup=False


    '''
    Will remove any frames on the grid and then place the requested frame on the grid
    '''
    def showwindow(self, frame_name):
        if not self.ignore_setup:
            
            #print(self.frames)
            for frame in self.frames:
                self.frames[frame].frame.grid_forget()
                print(self.frames[frame])
            self.current_frame = frame_name
            frame = self.frames[frame_name]
            self.current_frame_object = frame
            frame.frame.grid(row=0,column=0)
            self.frame_obj.update()



    '''
    Class to create a frame which can be scrolled (usually used for listing items on the window etc.)
    A special class needs to be used because to create a scrollable frame in tkinter, it must be
    placed on a canvas which must be linked to a scrollbar.
    '''
    class CreateScrollableFrame(ttk.Frame):

        def __init__(self,parent,row=0, column=0,columnspan=1,rowspan=1, height=0, width=0, border_text="",padx=15,pady=5):
            super().__init__(parent.container)
            self.parent=parent


            self.scrollable_canvas = tk.Canvas(parent.container, bd=0, highlightthickness=0)
            self.scrollbar = ttk.Scrollbar(self.parent.container, orient="vertical", command=self.scrollable_canvas.yview)
            self.hscrollbar = ttk.Scrollbar(self.parent.container, orient="horizontal", command=self.scrollable_canvas.xview)

            self.scrollable_frame = ttk.Frame(self.scrollable_canvas)


            self.bind("<Configure>", lambda e: self.scrollable_canvas.configure(scrollregion = self.scrollable_canvas.bbox("all")))

            self.scrollable_canvas.create_window((0,0), window=self.scrollable_frame, anchor='nw')

            self.scrollable_canvas.configure(yscrollcommand=self.scrollbar.set)
            self.scrollable_canvas.configure(xscrollcommand=self.hscrollbar.set)
            self.hscrollbar.grid(row=1, column=0, sticky="ew")
            self.scrollbar.grid(row=0, column=1, sticky="ns")
            
            self.scrollable_canvas.grid(row=0, column=0, sticky="nsew")
            
            
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

        '''
        Changes the width of the canvas and master_container to the frame inside of it (used when the frame changes size).
        This is required because the canvas does not automatically change width. The canvas scroll region is also updated,
        and the adjust_scrollbar function is called (see function description).
        '''
        def update(self):
            self.parent.parent.update_idletasks()
            if self.parent.container.winfo_height() >= self.scrollable_frame.winfo_height()+20:
                self.vscrollable=False # scrollable parameter checked when user scrolls. Will prevent when False
            else:
                self.vscrollable=True

            self.scrollable_canvas.update_idletasks()
            self.scrollable_canvas.config(scrollregion=self.scrollable_frame.bbox())
            
        '''
        Removes the scrollbar if the frame size is big enough
        '''
        def adjust_scrollbar(self,event):
            self.parent.parent.update_idletasks()
            self.scrollable_frame.update()

                
            if self.parent.container.winfo_height() >= self.scrollable_frame.winfo_height()+20:
                self.vscrollable=False # scrollable parameter checked when user scrolls. Will prevent when False
            else:
                self.vscrollable=True


if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    parent = tk.Toplevel(master=root)
    root.title("Training App")

    parent.tk.call("source", "sun-valley.tcl")
    parent.tk.call("set_theme", "light")
    
    tracker = Tracker(parent)
    tracker.bind_config()

    gui = GUI(parent,tracker)


    parent.mainloop()