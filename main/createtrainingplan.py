from random import randint
import datetime

class Set():
    def __init__(self,controller,exercise_obj,index):
        self.controller=controller
        self.exercise_obj=exercise_obj
        # a variable which when toggled, will isntruct the user to complete the exercise on both arms/legs.
        # will only be toggled if the "type" description is that of an exercise where this is required (see descriptions
        # below)
        self.eachside=False 

        self.reps=0
        self.time=0 # seconds
        self.distance=0 # meters

        # a type of exercise which is rep-based
        if self.exercise_obj.type==1 or self.exercise_obj.type==2:
            self.reps=10
        # a type of exercise which is time based
        if self.exercise_obj.type==3 or self.exercise_obj.type==4:
            self.time=45
        # a type of exercise which is distance based
        if self.exercise_obj.type==5:
            self.distance=50
        
        self.controller.controller.trainingplanjson["circuits"][-1]["supersets"][-1]["sets"].append({"exercise_id":self.exercise_obj.ID, "name": self.exercise_obj.descriptor, "reps":self.reps,"time":self.time,"distance":self.distance})
class Superset():
    def __init__(self,controller, index, sets):
        self.controller=controller
        

        for i in range(sets):
            random_no = randint(0,len(self.controller.controller.validexerciseIDs)-1)
            set=Set(self, self.controller.controller.master_controller.exercisedata_dict[self.controller.controller.validexerciseIDs[random_no]],index)
        

class Circuit():
    def __init__(self,controller, sets, supersets):
        self.controller=controller
        self.controller.trainingplanjson["circuits"][-1]["supersets"] = []

        for i in range(supersets):
            supersetname = f"Superset {i+1}"

            self.controller.trainingplanjson["circuits"][-1]["supersets"].append({"superset_name":supersetname, "sets":[]})

            superset = Superset(controller, i, sets)


class SessionPlan():
    def __init__(self, controller,sets,supersets,circuits, planned_date):
        self.controller=controller
        self.exercises = []

        # all of the session plan data will be stored in this JSON
        self.trainingplanjson = {"circuits":[],"warmup":[],"cooldown":[],"customerid":"", "timestamp":datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "planned_date": str(planned_date)}

        for i in range(circuits):
            circuitname = f"Circuit {i+1}"
            self.trainingplanjson["circuits"].append({"circuit_name":circuitname})

            circuit = Circuit(self, sets, supersets)
            self.exercises.append(circuit)

        


class TrainingPlanCreator():
    

    def __init__(self, customer, master_controller):
        self.customer=customer
        self.master_controller=master_controller
    

    def createtrainingplan(self, sets,circuits,supersets, planned_date):
        self.validexerciseIDs = []
        for exercise_id in self.master_controller.exercisedata_dict:
            exercise = self.master_controller.exercisedata_dict[exercise_id]
            if exercise.category in self.customer.categories:
                self.validexerciseIDs.append(exercise_id)
    
        

        self.sessionplan = SessionPlan(self, sets,supersets,circuits, planned_date)
        self.customer.session_plans.append(self.sessionplan.trainingplanjson)
        self.customer.writetofile()
        
