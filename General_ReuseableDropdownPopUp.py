import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkcalendar import Calendar


def dropdownselectioncomplete(complete_function, options, window):
    
    window.destroy()
    complete_function(options.get())

def dropdownselect(complete_function, text, choices):
    
    dropdown_window = tk.Tk() #new window popup
    dropdown_window.title('Select Category') #naming the window
    info_text = tk.Label(dropdown_window, text=text, fg='black')
    info_text.pack()

    variable = StringVar(dropdown_window)
    variable.set("Make a selection") # default value

    w = OptionMenu(dropdown_window, variable, *choices)
    w.pack()

    b = Button(dropdown_window, text="OK", command=lambda:dropdownselectioncomplete(complete_function,variable, dropdown_window))
    b.pack(pady=5)

