from tkinter import ttk
import tkinter as tk

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
                row=0
                for setindex,set in enumerate(self.controller.controller.trainingplanjson["circuits"][circuitindex]["supersets"][supersetindex]['sets']):
                    self.ListSets(self,supersetindex,setindex,row,circuitindex)
                    row+=2

            class ListSets():
                """
                Will list all of the sets inside of a superset frame (which is inside of a circuit frame)
                """
                def __init__(self,controller,supersertindex,setindex,row, circuitindex):
                    self.controller=controller
                    print(self.controller.controller.controller.trainingplanjson['circuits'][circuitindex]['supersets'][supersertindex])
                    self.set_label = ttk.Label(self.controller.frame,text=f"Set {supersertindex+1}: {self.controller.controller.controller.trainingplanjson['circuits'][circuitindex]['supersets'][supersertindex]['sets'][setindex]['name']}")
                    self.set_label.grid(row=row,column=0,padx=10,pady=(10,3),sticky="w")
                    if self.controller.controller.controller.trainingplanjson['circuits'][circuitindex]['supersets'][supersertindex]['sets'][setindex]['reps'] != 0:
                        self.info_label = ttk.Label(self.controller.frame,text=f"Reps: {self.controller.controller.controller.trainingplanjson['circuits'][circuitindex]['supersets'][supersertindex]['sets'][setindex]['reps']}")
                    elif self.controller.controller.controller.trainingplanjson['circuits'][circuitindex]['supersets'][supersertindex]['sets'][setindex]['time'] != 0:
                        self.info_label = ttk.Label(self.controller.frame,text=f"Time: {self.controller.controller.controller.trainingplanjson['circuits'][circuitindex]['supersets'][supersertindex]['sets'][setindex]['time']}")
                    elif self.controller.controller.controller.trainingplanjson['circuits'][circuitindex]['supersets'][supersertindex]['sets'][setindex]['distance'] != 0:
                        self.info_label = ttk.Label(self.controller.frame,text=f"Distance: {self.controller.controller.controller.trainingplanjson['circuits'][circuitindex]['supersets'][supersertindex]['sets'][setindex]['distance']}m")
                    else:self.info_label = ttk.Label(self.controller.frame,text=f"Unknown reps")
                    self.info_label.grid(row=row+1, column=0,padx=10,pady=(0,6),sticky="w")


    def savedata(self):
        if self.saved == False:
            self.customer.session_plans.append(self.trainingplanjson)
        else:
            self.customer.session_plans.remove[-1]
            self.customer.session_plans.append(self.trainingplanjson)

        self.customer.writetofile()

    def injectdata(self,trainingplanjson, customer):
        self.customer=customer
        self.trainingplanjson = trainingplanjson
        self.saved=False
        try:
            self.master_frame.grid_forget()
            self.master_frame.destroy()
        except Exception as e: pass
        
        self.master_frame = ttk.Frame(self.frame)
        self.master_frame.grid(row=1,column=0)

        column=0
        row=0
        for i,self.circuit in enumerate(self.trainingplanjson["circuits"]):
            self.ListCircuit(self,i, row, column)
            column+=1
            


    def __init__(self, controller):
        # initial setup
        tk.Frame.__init__(self)
        self.controller = controller
        self.frame = ttk.Frame(self.controller.frame_obj.scrollable_frame)
        
        
        self.save_button = ttk.Button(self.frame,text="Save",command=self.savedata)
        self.save_button.grid(row=0,column=0)
