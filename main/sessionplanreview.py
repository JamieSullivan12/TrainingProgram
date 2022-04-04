from email import message
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
class SessionPlanReviewPage(tk.Frame):
    def set_heading(self):
        self.controller.tkRoot.title("Training App > Edit Customer Data")
    

    class ListCircuit():
        """
        Will list all the circuits across the page
        """
        def __init__(self,controller,index,row,column):
            self.controller=controller

            self.frame = ttk.LabelFrame(self.controller.master_frame,text=self.controller.trainingplanjson["circuits"][index]["circuit_name"])
            self.frame.grid(row=row,column=column,padx=15,pady=15)

            row=0
            for supersetindex,self.superset in enumerate(self.controller.trainingplanjson["circuits"][index]["supersets"]):
                self.ListSupersets(self,supersetindex,index,row)
                row += 1
        
        class ListSupersets():
            """
            Will list all of the supersets inside of a circuit frame
            """
            def __init__(self,controller,supersetindex,circuitindex,row):
                self.controller=controller

                self.frame=ttk.LabelFrame(self.controller.frame,text=f"Superset {supersetindex+1}")
                self.frame.grid(row=row,column=0,padx=10,pady=(15,0),sticky="ew")


                for setindex,set in enumerate(self.controller.controller.trainingplanjson["circuits"][circuitindex]["supersets"][supersetindex]['sets']):
                    self.ListSets(self,supersetindex,setindex,circuitindex)


            class ListSets():
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
                

                def __init__(self,controller,supersetindex,setindex, circuitindex):
                    # Each set shows up like this:
                    # Set #: set_name {set}
                    # Reps/Time/Distance: # {info}
                    
                    self.controller=controller

                    # container frame for an individual set
                    self.set_frame = ttk.Frame(self.controller.frame)

                    # provide pathways to the set in the JSON object (used for reading and modification)
                    self.supersetindex=supersetindex
                    self.setindex=setindex
                    self.circuitindex=circuitindex

                    # creating the set label (e.g. Set 1: Barbell Squats)
                    self.set_label = ttk.Label(self.set_frame,text=f"Set {self.setindex+1}: {self.controller.controller.controller.trainingplanjson['circuits'][self.circuitindex]['supersets'][self.supersetindex]['sets'][self.setindex]['name']}")
                    
                    # creating the info display (e.g. Reps: 10 OR Time: 30)
                    self.type_of_exercise=""
                    if self.controller.controller.controller.trainingplanjson['circuits'][circuitindex]['supersets'][supersetindex]['sets'][setindex]['reps'] != 0:
                        self.type_of_exercise="reps"
                    elif self.controller.controller.controller.trainingplanjson['circuits'][circuitindex]['supersets'][supersetindex]['sets'][setindex]['time'] != 0:
                        self.type_of_exercise="time"
                    elif self.controller.controller.controller.trainingplanjson['circuits'][circuitindex]['supersets'][supersetindex]['sets'][setindex]['distance'] != 0:
                        self.type_of_exercise="distance"
                    else:
                        self.type_of_exercise="reps"

                    self.info_label = ttk.Label(self.set_frame,text=f"{self.type_of_exercise.title()}: {self.controller.controller.controller.trainingplanjson['circuits'][circuitindex]['supersets'][supersetindex]['sets'][setindex][self.type_of_exercise]}")
                    
            
                    self.set_label.grid(row=0,column=0,padx=10,pady=(10,3),sticky="w")
                    self.info_label.grid(row=1, column=0,padx=10,pady=(0,6),sticky="w")
                    self.set_frame.grid(row=setindex+1, column=0,sticky="w")

                    self.bindframe(self.set_label,"<Double-Button-1>",self.setchangerequest)
                    self.bindframe(self.info_label,"<Double-Button-1>",self.infochangerequest)


                def setchangerequest(self,event):
                    """
                    Will replace the set desciptor with an Entry box (pre-filled with existing set value) so the user can change it
                    """
                    self.set_label.grid_forget()

                    self.set_entry = ttk.Entry(self.set_frame)
                    self.set_entry.insert(tk.END, self.controller.controller.controller.trainingplanjson['circuits'][self.circuitindex]['supersets'][self.supersetindex]['sets'][self.setindex]['name'])
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
                    self.info_entry.insert(tk.END, self.controller.controller.controller.trainingplanjson['circuits'][self.circuitindex]['supersets'][self.supersetindex]['sets'][self.setindex][self.type_of_exercise])
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
                    # insert a new exercise_id for that set (it will be 0 as it is a custom ID)
                    self.controller.controller.controller.trainingplanjson['circuits'][self.circuitindex]['supersets'][self.supersetindex]['sets'][self.setindex]['exercise_id'] = 0
                    # insert a new exercise name for that set (whatever the user entered)
                    self.controller.controller.controller.trainingplanjson['circuits'][self.circuitindex]['supersets'][self.supersetindex]['sets'][self.setindex]['name'] = new_text
                    # change the set label to include the new defined value. This label will be shown in the setcancelrequest() function (which also removes the entry widget)
                    self.set_label["text"] = f"Set {self.setindex+1}: {new_text}"
                    self.setcancelrequest()
                
                def infoapplychanges(self,event):
                    """
                    Apply user-defined changes in the Entry box to the JSON (note: this does not change them in secondary storage. The user must press "Save" to do so)
                    """
                    # entry widget string value (what the user has entered)
                    new_text=self.info_entry.get()
                    # insert a new value for the exercise reps/distance/time into the JSON
                    self.controller.controller.controller.trainingplanjson['circuits'][self.circuitindex]['supersets'][self.supersetindex]['sets'][self.setindex][self.type_of_exercise]=new_text
                    # change the set label to include the new defined value. This label will be shown in the infocancelrequest() function (which also removes the entry widget)
                    self.info_label["text"] = f"{self.type_of_exercise.title()}: {new_text}"
                    self.infocancelrequest()



    def savedata(self):
        """
        Calls a function in the customer object which applies the new JSON to secondary memory
        """

        self.customer.removesessionplan(self.trainingplanjson)
        self.customer.session_plans.append(self.trainingplanjson)
        self.customer.writetofile()

    def export_pdf(self):
        import createpdf
        from tkinter.filedialog import askdirectory

        directory = ""
        directory = askdirectory()
        print(directory)
        if directory != "":
            try:
                createpdf.createsessionplanPDF(self.trainingplanjson, self.customer.name, directory)
            except Exception as e:
                messagebox.showerror(title="ERROR", message=f"An error occured when exporting to PDF:\n\n{str(e)}")
    
    def completedatechange(self,date):
        self.trainingplanjson["planned_date"] = str(date)
        self.savedata()
        self.injectdata(self.trainingplanjson, self.customer)
    def changeplanneddate(self):
        import selectdate

        selectdate.dateselect("Select Date", self.completedatechange)

    def __init__(self, controller):
        # initial setup
        tk.Frame.__init__(self)
        self.controller = controller
        self.frame = ttk.Frame(self.controller.frame_obj.scrollable_frame)

        self.info_label = ttk.Label(self.frame)
        self.info_label.grid(row=0,column=0,columnspan=100, sticky="w", padx=15, pady=15)
        self.save_button = ttk.Button(self.frame,text="Save",command=self.savedata)
        self.save_button.grid(row=1,column=0,ipadx=15,columnspan=100, padx=15, pady=5, sticky="w")

        self.pdf_export_button = ttk.Button(self.frame,text="Export PDF",command=self.export_pdf)
        self.pdf_export_button.grid(row=2,column=0,columnspan=100,ipadx=15, padx=15, pady=5, sticky="w")

        self.change_planned_date_button = ttk.Button(self.frame,text="Change Planned Date",command=self.changeplanneddate)
        self.change_planned_date_button.grid(row=3,column=0,columnspan=100,ipadx=15, padx=15, pady=5, sticky="w")


    def injectdata(self,trainingplanjson, customer):
        """
        Inject specific session plan data in to this page.
        Params:
        - trainingplanjson: the generated/stored JSON for the session plan
        - customer: the customer object for the specific customer that the session plan was made for
        """
        
        self.customer=customer
        self.trainingplanjson = trainingplanjson

        try:
            self.master_frame.grid_forget()
            self.master_frame.destroy()
        except Exception as e: pass        
        self.master_frame = ttk.Frame(self.frame)
        self.master_frame.grid(row=5,column=0)

        self.info_label["text"] = f"Session Plan for {self.customer.name}\nLast modified: {self.trainingplanjson['timestamp']}\nPlanned date: {self.trainingplanjson['planned_date']}"

        # list all circuits across the page
        column=0
        row=0
        for i,self.circuit in enumerate(self.trainingplanjson["circuits"]):
            self.ListCircuit(self,i, row, column)
            column+=1