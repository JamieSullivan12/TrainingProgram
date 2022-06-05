from email import message
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
class SessionPlanReviewPage(ttk.Frame):

    class ListCircuit():
        """
        Will list all the circuits across the page
        """
        def __init__(self, page_frame, circuit_obj,column):

            self.circuit_frame = ttk.LabelFrame(page_frame,text=f"Circuit {column+1}")
            self.circuit_frame.grid(row=0,column=column,padx=15,pady=15)


            for superset_index, superset_obj in enumerate(circuit_obj.supersets):
                self.ListSupersets(self.circuit_frame,superset_obj, superset_index)

        

        class ListSupersets():
            """
            Will list all of the supersets inside of a circuit frame
            """
            def __init__(self,circuit_frame,superset_obj,superset_index):
                
                self.superset_frame=ttk.LabelFrame(circuit_frame,text=f"Superset {superset_index+1}")
                self.superset_frame.grid(row=superset_index,column=0,padx=10,pady=(15,0),sticky="ew")


                for set_index,set_obj in enumerate(superset_obj.sets):
                    self.ListExercises(self.superset_frame,set_obj,set_index)


            class ListExercises():
                """
                Controls the creation of a single set in the session plan review page. Abstracts functionality:
                - Showing the set as well as reps/time/distance
                - Allow for set modification (by double clicking on the field that needs changing)
                """

                def bindframe(self,frame,sequence,func):
                    """
                    Used to bind a click event to a function
                    """
                    frame.bind(sequence, func)
                    for child in frame.winfo_children():
                        child.bind(sequence, func)
                

                def __init__(self, superset_frame, set_obj, set_index):
                    self.set_index = set_index
                    # container frame for an individual set
                    self.set_frame = ttk.Frame(superset_frame)
                    self.set_obj=set_obj
                    self.setname = ""
                    self.setlength = ""
                    self.typeofexercise=""

                    if self.set_obj.overridename != "": 
                        self.setname=self.set_obj.overridename
                    else:
                        self.setname=self.set_obj.exercise_obj.descriptor
                    
                    if self.set_obj.overridelength != str(0): 
                        self.setlength=self.set_obj.overridelength
                        self.typeofexercise="custom"
                    else:
                        # creating the info display (e.g. Reps: 10 OR Time: 30)
                        if str(self.set_obj.reps) != str(0):
                            self.typeofexercise="reps"
                            self.setlength = str(self.set_obj.reps)
                        elif str(self.set_obj.time) != str(0):
                            self.typeofexercise="time"
                            self.setlength = str(self.set_obj.time)
                        elif str(self.set_obj.distance) != str(0):
                            self.typeofexercise="distance"
                            self.setlength = str(self.set_obj.distance)

                    # creating the set label (e.g. Set 1: Barbell Squats)
                    self.set_label = ttk.Label(self.set_frame,text=f"Set {set_index+1}: {self.setname}")

                    self.info_label = ttk.Label(self.set_frame,text=f"{self.typeofexercise.title()}: {self.setlength}")
                    
            
                    self.set_label.grid(row=0,column=0,padx=10,pady=(10,3),sticky="w")
                    self.info_label.grid(row=1, column=0,padx=10,pady=(0,6),sticky="w")
                    self.set_frame.grid(row=set_index+1, column=0,sticky="w")

                    self.bindframe(self.set_label,"<Double-Button-1>",self.setchangerequest)
                    self.bindframe(self.info_label,"<Double-Button-1>",self.infochangerequest)



                def setchangerequest(self,event):
                    """
                    Will replace the set desciptor with an Entry box (pre-filled with existing set value) so the user can change it
                    """
                    self.set_label.grid_forget()


                    self.set_entry = ttk.Entry(self.set_frame)
                    self.set_entry.insert(tk.END, self.setname)
                    self.set_entry.grid(row=0,column=0,sticky="w",padx=10,pady=(10,3))

                    # bind return (save changes) and escape (cancel changes) keys
                    self.set_entry.bind("<Return>",self.setapplychanges)
                    self.set_entry.bind("<Escape>",self.setcancelrequest)

                def infochangerequest(self,event):
                    """
                    Will replace the set information text with an Entry box (pre-filled with existing set value) so the user can change it
                    """
                    self.info_label.grid_forget()
                    self.info_entry = ttk.Entry(self.set_frame)
                    self.info_entry.insert(tk.END, self.setlength)
                    self.info_entry.grid(row=1,column=0,sticky="w",padx=10,pady=(0,6))

                    # bind return (save changes) and escape (cancel changes) keys
                    self.info_entry.bind("<Return>",self.infoapplychanges)
                    self.info_entry.bind("<Escape>",self.infocancelrequest)

                def setcancelrequest(self,*args):
                    """
                    Will replace existing entry box for the set desciptor with the original text. Note this function can be called when:
                    - the user pressing escape (whereby the function is directly called, destroys entry boxes - cancelling changes)
                    - the user pressing return (which first directs to another function - setapplychanges - which will add the new user-defined value to the JSON)
                    """
                    self.set_entry.destroy()
                    self.set_label.grid(row=0,column=0,sticky="w",padx=10,pady=(10,3))
                    
                def infocancelrequest(self,*args):
                    """
                    Will replace existing entry box for the set information text entry with the original text. Note this function can be called when:
                    - the user pressing escape (whereby the function is directly called, destroys entry boxes - cancelling changes)
                    - the user pressing return (which first directs to another function - infoapplychanges - which will add the new user-defined value to the JSON)
                    """
                    self.info_entry.destroy()
                    self.info_label.grid(row=1,column=0,sticky="w",padx=10,pady=(0,6))

                def setapplychanges(self,event):
                    """
                    Apply user-defined changes in the Entry box to the JSON (note: this does not change them in secondary storage. The user must press "Save" to do so)
                    """
                    # entry widget string value (what the user has entered)
                    new_text=self.set_entry.get()

                    # insert a new exercise name for that set (whatever the user entered)
                    self.set_obj.overridename = new_text
                    # change the set label to include the new defined value. This label will be shown in the setcancelrequest() function (which also removes the entry widget)
                    self.set_label["text"] = f"Set {self.set_index+1}: {new_text}"
                    self.setcancelrequest()
                
                def infoapplychanges(self,event):
                    """
                    Apply user-defined changes in the Entry box to the JSON (note: this does not change them in secondary storage. The user must press "Save" to do so)
                    """
                    # entry widget string value (what the user has entered)
                    new_text=self.info_entry.get()
                    # insert a new value for the exercise reps/distance/time into the JSON
                    self.set_obj.overridelength=new_text
                    # change the set label to include the new defined value. This label will be shown in the infocancelrequest() function (which also removes the entry widget)
                    self.info_label["text"] = f"{new_text}"
                    self.infocancelrequest()



    def savedata(self):
        """
        Calls a function in the customer object which applies the new JSON to secondary memory
        """


        self.customer.writetofile()

    def export_pdf(self):
        import Process_GeneratePDF
        from tkinter.filedialog import askdirectory

        directory = ""
        directory = askdirectory()
        print(directory)
        if directory != "":
            try:
                Process_GeneratePDF.createsessionplanPDF(self.trainingplan, self.customer.name, directory)
            except Exception as e:
                messagebox.showerror(title="ERROR", message=f"An error occured when exporting to PDF:\n\n{str(e)}")
    
    def completedatechange(self,date):

        self.trainingplan.planned_date = str(date)
        self.savedata()
        self.injectdata(self.trainingplan, self.customer)
    
    def changeplanneddate(self):
        import reuseable_datepopup

        reuseable_datepopup.dateselect("Select Date", self.completedatechange)

    def __init__(self, controller):
        ttk.Frame.__init__(self, controller.frame_obj.scrollable_frame)

        self.controller = controller

        self.info_label = ttk.Label(self)
        self.info_label.grid(row=0,column=0,columnspan=100, sticky="w", padx=15, pady=15)
        self.save_button = ttk.Button(self,text="Save",command=self.savedata)
        self.save_button.grid(row=1,column=0,ipadx=15,columnspan=100, padx=15, pady=5, sticky="w")

        self.pdf_export_button = ttk.Button(self,text="Export PDF",command=self.export_pdf)
        self.pdf_export_button.grid(row=2,column=0,columnspan=100,ipadx=15, padx=15, pady=5, sticky="w")

        self.change_planned_date_button = ttk.Button(self,text="Change Planned Date",command=self.changeplanneddate)
        self.change_planned_date_button.grid(row=3,column=0,columnspan=100,ipadx=15, padx=15, pady=5, sticky="w")


    def injectdata(self,trainingplan, customer):
        """
        Inject specific session plan data in to this page.
        Params:
        - trainingplanjson: the generated/stored JSON for the session plan
        - customer: the customer object for the specific customer that the session plan was made for
        """
        
        self.customer=customer
        self.trainingplan=trainingplan

        try:
            self.master_frame.grid_forget()
            self.master_frame.destroy()
        except Exception as e: pass        
        self.master_frame = ttk.Frame(self)
        self.master_frame.grid(row=5,column=0)

        self.info_label["text"] = f"Session Plan for {self.customer.name}\nLast modified: {self.trainingplan.timestamp}\nPlanned date: {self.trainingplan.planned_date}"

        # list all circuits across the page
        for column,circuit in enumerate(self.trainingplan.circuits):
            self.ListCircuit(self.master_frame, circuit, column)
