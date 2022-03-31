import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar


def dateselectioncomplete(cal, window, complete_function):
    window.destroy()
    date = cal.selection_get()
    complete_function(date)


def dateselect(text, complete_function):
    calendar_window = tk.Tk() #new window popup
    calendar_window.title('Settlement Date') #naming the window
    info_text = tk.Label(calendar_window, text=text, fg='black')
    info_text.pack()
    cal = Calendar(calendar_window, font='Helvlevtica 14', selectmode="day", CalendarSelected="date_selected") #creating a calendar object - selectmode='day' means that the user can select a day
    cal.pack(fill="both",expand=True) #adding it to the new window
    ok_button = ttk.Button(calendar_window,text='continue',style="Accent.TButton",width=20,command=lambda:dateselectioncomplete(cal, calendar_window, complete_function)) #The OK button to submit the date selection
    ok_button.pack()