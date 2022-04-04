from random import randint
import datetime
from tokenize import Triple
from tkinter import messagebox



class TrainingPlanCreator():

    def round(self,x, base=5):
        return base * round(x/base)

    def Sets(self, number_of_sets):
        if len(self.validexerciseIDs) == 0:
            self.error = True
            return
    
        
        # create sets
        for i in range(number_of_sets):
            random_no = randint(0,len(self.validexerciseIDs)-1)
            exercise_obj = self.master_controller.exercisedata_dict[self.validexerciseIDs[random_no]]

            del self.validexerciseIDs[random_no]
            # some exercises will have the following methods of completion: (reps, time, distance)
            # for example:
            # - pushups is reps based (e.g., 10x pushups)
            # - plank is time based (e.g., 30s plank)
            # - sprinting is distance based (e.g., 100m sprint)
            reps=0
            time=0 # seconds
            distance=0 # meters

            # the method of completion (reps, time distance) is defined by the "type" parameter in the Exercises database
            # NOTE: only the method of the selected exercise will be populated with a value. all others will be 0
            if exercise_obj.type==1 or exercise_obj.type==2:
                reps=self.round(10*self.customer.ability_level,base=5)
            elif exercise_obj.type==3 or exercise_obj.type==4:
                time=self.round(20*self.customer.ability_level, base=5)
            elif exercise_obj.type==5:
                distance=self.round(25*self.customer.ability_level,base=5)

            self.trainingplanjson["circuits"][-1]["supersets"][-1]["sets"].append({"exercise_id":exercise_obj.ID, "name": exercise_obj.descriptor, "reps":reps,"time":time,"distance":distance})

    def Supersets(self, number_of_supersets, number_of_sets):
        self.trainingplanjson["circuits"][-1]["supersets"] = []
        # create supersets
        for i in range(number_of_supersets):
            # add the superset to the JSON
            supersetname = f"Superset {i+1}"
            self.trainingplanjson["circuits"][-1]["supersets"].append({"superset_name":supersetname, "sets":[]})
            self.Sets(number_of_sets)

        
    def Circuits(self, number_of_circuits, number_of_supersets, number_of_sets):

        for i in range(number_of_circuits):
            circuitname = f"Circuit {i+1}"
            self.trainingplanjson["circuits"].append({"circuit_name":circuitname})
            self.Supersets(number_of_supersets, number_of_sets)


    def __init__(self, customer, master_controller):
        """
        Constructor for TrainingPlanCreator()
        - customer is the Customer object (containing details - including selected goals - concerning the 
            customer for whom the training plan is being made)
        - master_controller is the least abstract object of the program. Contains all data objects like
            ExerciseData and CategoriesData
        """
        self.customer=customer
        self.master_controller=master_controller

    def createtrainingplan(self, number_of_sets,number_of_circuits,number_of_supersets, planned_date):
        # create an array of exercises that are within the selected user goals
        # NOTE: these will be the only exercises used in the generation of the training plan
        self.validexerciseIDs = []
        for exercise_id in self.master_controller.exercisedata_dict:
            exercise = self.master_controller.exercisedata_dict[exercise_id]
            if exercise.category in self.customer.categories:
                self.validexerciseIDs.append(exercise_id)
        self.error=False
        self.sets = []    
        

        # initialising the JSON with circuits, warmup, cooldown, customerid, timestamp (current time), and planned date (the date that the trainer
        # is planning on completing the session)
        self.trainingplanjson = {"circuits":[],"warmup":[],"cooldown":[],"customerid":"", "timestamp":datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "planned_date": str(planned_date)}

        self.Circuits(number_of_circuits,number_of_supersets,number_of_sets)

        if self.error == True:
            result = messagebox.askyesno(title="WARNING", message="There are not enough exercises to fill the requested training plan structure\n\nPlease either select more goals or decrease training plan size.\n\nWould you like to ignore this message?")
            if result == True:
                # add the session plan to the customer's session plans list (in the customer object)
                self.customer.session_plans.append(self.trainingplanjson)
                # save changes
                self.customer.writetofile()
        
