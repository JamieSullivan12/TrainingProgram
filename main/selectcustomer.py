import tkinter as tk
from tkinter import ttk
class SelectCustomerPage(ttk.Frame):
    def set_heading(self):
        self.controller.root.title("Training Program")

    def search(self):
        search = self.search_texbox.get()
        for


    def __init__(self, controller):
        tk.Frame.__init__(self)
        self.controller = controller

        self.frame=ttk.Frame(self.controller.frame_obj.scrollable_frame)

        ## creating a scrollable frame using function defined in app.py
        #self.frame = controller.CreateScrollableFrame(self.controller,row=1,column=0,border_text="",padx=15,pady=(15,0))


        header = ttk.Label(self.frame,text="Search Customer")
        header.grid(row=0,column=0,sticky="nw",padx=35,pady=(20,0))

        self.search_texbox = ttk.Entry(self.frame, width=50)
        self.search_texbox.grid(row=1,column=0)
        
        self.funding_button = ttk.Button(self.frame,text="Search", width=30,command=lambda:self.search())
        self.funding_button.grid(row=1,column=1, padx=(20,10),pady=10)

