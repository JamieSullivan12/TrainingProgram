# -------------------------------------------
# creates the home page once initialised
# -------------------------------------------

import tkinter as tk
from tkinter import ttk
class HomePage(ttk.Frame):
    def set_heading(self):
        self.controller.root.title("Training Program > Home")
    def __init__(self, controller):
        tk.Frame.__init__(self)
        self.controller = controller

        self.frame=ttk.Frame(self.controller.frame_obj.scrollable_frame)

        ## creating a scrollable frame using function defined in app.py
        #self.frame = controller.CreateScrollableFrame(self.controller,row=1,column=0,border_text="",padx=15,pady=(15,0))


        header = ttk.Label(self.frame,text="Training App")
        header.grid(row=0,column=0,sticky="nw",padx=35,pady=(20,0))
        
        self.funding_button = ttk.Button(self.frame,text="Customer Page", width=30,command=lambda:self.controller.showwindow("CustomerPage"))
        self.funding_button.grid(row=1,column=0, padx=(20,10),pady=10)

        self.monthend_button = ttk.Button(self.frame,text="Placeholder12",width=30)
        self.monthend_button.grid(row=2,column=0, padx=(20,10),pady=10)
