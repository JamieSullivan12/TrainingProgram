from random import randint
import datetime
from tokenize import Triple
from tkinter import messagebox
from typing import Set
import json
from numpy import number


class TrainingPlan():

    def __init__(self, master_controller, traineeobj, planned_date = ""):
        # assigning attributes specific to this training plan
        self.traineeobj = traineeobj

        self.circuits = []
        self.timestamp = str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        self.planned_date = planned_date
        self.validexerciseIDs=[]
        self.cooldownexerciseIDs = []
        self.validexerciseIDs = []

        self.master_controller=master_controller
        self.not_enough_exercises_error=False

    class Set():
        def round(self,x, base=5):
            return base * round(x/base)

        def __init__(self, parent_controller, exercisedataset, override_data=""):

            """Will create a requested number of sets based on the following parameters:
            - number_of_sets: number of sets to exist WITHIN a SINGLE SUPERSET
            Note: exercises for each set will be chosen randomly. Duplicates are avoided"""

            self.parent_controller=parent_controller


            # the type of length of a set (reps, time distance) are defined by the "type" parameter in the ExerciseData database (1,2=reps, 3,4=time, 5=distance, 6=long run)
            self.reps=0 # repetitions
            self.time=0 # seconds
            self.distance=0 # meters
            self.overridelength = "0"
            self.overridename = ""

            changelength=""
            if override_data != "":
                if override_data["OverrideName"] != "": self.overridename = override_data["OverrideName"]
                if override_data["OverrideLength"] != "": self.overridelength = override_data["OverrideLength"]

                for exercise_id in self.parent_controller.master_controller.exercisedata_dict:
                    exercise = self.parent_controller.master_controller.exercisedata_dict[exercise_id]

                    if str(exercise.ID) == override_data["ID"]:
                        self.exercise_obj = exercise
                changelength = override_data["Length"]


            else:
                # check if there are enough exercises left in the database to fill the requested number of circuits/supersets/sets.
                if len(exercisedataset) <= parent_controller.total_number_of_exercises:
                    parent_controller.not_enough_exercises_error = True
                    return

                # choose a random exercise from the available selection (using randint library)
                random_no = randint(0,len(exercisedataset)-1)
                self.exercise_obj = self.parent_controller.master_controller.exercisedata_dict[exercisedataset[random_no]]
                # remove the randomly chosen exercise from the dictionary of possible exercises for this training plan. This is so that it is not duplicated.
                del exercisedataset[random_no]

            if str(self.overridelength) != 0 and str(self.overridelength) != "" and str(self.overridelength) != None:
                if self.exercise_obj.type==1 or self.exercise_obj.type==2:
                    self.reps=str(self.round(10*self.parent_controller.traineeobj.ability_level,base=5))
                    if changelength != "": self.reps=changelength
                elif self.exercise_obj.type==3 or self.exercise_obj.type==4:
                    self.time=str(self.round(20*self.parent_controller.traineeobj.ability_level, base=5))
                    if changelength != "": self.time=changelength
                elif self.exercise_obj.type==5:
                    self.distance=str(self.round(25*self.parent_controller.traineeobj.ability_level,base=5))
                    if changelength != "": self.distance=changelength
                elif self.exercise_obj.type == 6:
                    self.distance=str(self.round(150*self.parent_controller.traineeobj.ability_level,base=100))
                    if changelength != "": self.distance=changelength

        def getexerciselength(self):
            if str(self.reps) != "0" : return self.reps
            if str(self.time) != "0" : return self.time
            if str(self.distance) != "0": return self.distance
            if str(self.otherlength) != "0": return self.otherlength
            return None

    class Superset():
        def __init__(self, parent_controller, exercisedataset, override_data = ""):
            self.sets = []

            if override_data != "":
                for set in override_data["sets"]:
                    self.sets.append(parent_controller.Set(parent_controller, exercisedataset, override_data=set))
            
            else:
                count = 0
                while count < parent_controller.number_of_sets:
                    self.sets.append(parent_controller.Set(parent_controller, exercisedataset))
                    count = count + 1

    class Circuit():
        def __init__(self, parent_controller, exercisedataset, override_data = ""):
            self.supersets = []

            if override_data != "":
                for superset in override_data["supersets"]:
                    self.supersets.append(parent_controller.Superset(parent_controller, exercisedataset, override_data=superset))
            else:
                count = 0
                while count < parent_controller.number_of_supersets:
                    self.supersets.append(parent_controller.Superset(parent_controller, exercisedataset))
                    count = count + 1

    def generate_training_plan(self, number_of_sets, number_of_supersets, number_of_circuits,):

        self.number_of_sets = number_of_sets
        self.number_of_supersets = number_of_supersets
        self.number_of_circuits = number_of_circuits

        self.total_number_of_exercises = 0

        for exercise_id in self.master_controller.exercisedata_dict:
            exercise = self.master_controller.exercisedata_dict[exercise_id]

            if exercise.category in self.traineeobj.goals:
                self.validexerciseIDs.append(exercise_id)

        count = 0
        while count < self.number_of_circuits:
            self.circuits.append(self.Circuit(self, exercisedataset = self.validexerciseIDs))
            count = count + 1


        if self.not_enough_exercises_error == True:
            result = messagebox.showerror(title="WARNING", message="There are not enough exercises to fill the requested training plan structure\n\nPlease either select more goals or decrease training plan size.")
            return
        
        self.add_to_trainee()
        
    def add_to_trainee(self):
        self.traineeobj.training_plans.append(self)

    def export_to_string(self):
        self.exportstring = {"circuits":[],"customerid":str(self.traineeobj.ID), "timestamp":str(self.timestamp), "planned_date": str(self.planned_date)}


        for circ_count, circuit in enumerate(self.circuits):
            self.exportstring["circuits"].append({"supersets":[]})
            for super_count, superset in enumerate(circuit.supersets):
                self.exportstring["circuits"][circ_count]["supersets"].append({"sets":[]})
                for set_count, set in enumerate(superset.sets):
                    self.exportstring["circuits"][circ_count]["supersets"][super_count]["sets"].append({})
                    self.exportstring["circuits"][circ_count]["supersets"][super_count]["sets"][set_count] = {
                        "ID": str(set.exercise_obj.ID),
                        "Length": str(set.getexerciselength()),
                        "OverrideName": str(set.overridename),
                        "OverrideLength": str(set.overridelength)
                    } 
        return self.exportstring

    def import_from_string(self, importstring):
        self.importstring = importstring
        self.timestamp = importstring["timestamp"]
        self.planned_date = importstring["planned_date"]
        for circuit in self.importstring["circuits"]:
            print(circuit)
            self.circuits.append(self.Circuit(self, exercisedataset = self.master_controller.exercisedata_dict, override_data=circuit))
        self.export_to_string()




class TrainingPlanCreator():
    """
    An object which controls/manages the creation of a training plan for any Trainee
    In the constructor:
    - customer is the TraineeData object for whom the training plan is being generated. This is stored as metadata in the class, so that when the method to create the training plan is called, it can automatically be attributed to the pre-defined customer in the constructor.
    - master_controller is the top-level object (from the mainline). This object will include the data objects like ExerciseData and CategoryData 

    """
    def __init__(self, customer, master_controller):
        self.customer=customer
        self.master_controller=master_controller

    def round(self,x, base=5):
        return base * round(x/base)

    def Sets(self, number_of_sets, counter = 0):
        """Will create a requested number of sets based on the following parameters:
        - number_of_sets: number of sets to exist WITHIN a SINGLE SUPERSET
        Note: exercises for each set will be chosen randomly. Duplicates are avoided"""
        # base case for recursive algorithm
        if counter >= number_of_sets: return

        # check if there are enough exercises left in the database to fill the requested number of circuits/supersets/sets.
        if len(self.validexerciseIDs) == 0:
            self.not_enough_exercises_error = True
            return

        # choose a random exercise from the available selection (using randint library)
        random_no = randint(0,len(self.validexerciseIDs)-1)
        exercise_obj = self.master_controller.exercisedata_dict[self.validexerciseIDs[random_no]]
        # remove the randomly chosen exercise from the dictionary of possible exercises for this training plan. This is so that it is not duplicated.
        del self.validexerciseIDs[random_no]

        # the type of length of a set (reps, time distance) are defined by the "type" parameter in the ExerciseData database (1,2=reps, 3,4=time, 5=distance)
        reps="0" # repetitions
        time="0" # seconds
        distance="0" # meters
        if exercise_obj.type==1 or exercise_obj.type==2:
            reps=str(self.round(10*self.customer.ability_level,base=5))
        elif exercise_obj.type==3 or exercise_obj.type==4:
            time=str(self.round(20*self.customer.ability_level, base=5))
        elif exercise_obj.type==5:
            distance=str(self.round(25*self.customer.ability_level,base=5))

        # add the set to the Training Plan JSON object structure
        self.trainingplanjson["circuits"][-1]["supersets"][-1]["sets"].append({"exercise_id":str(exercise_obj.ID), "name": exercise_obj.descriptor, "reps":str(reps),"time":str(time),"distance":str(distance)})

        # recursive call (counter is increased to trigger base case)
        counter += 1
        self.Sets(number_of_sets, counter)

    def Supersets(self, number_of_supersets, number_of_sets, counter = 0):
        """
        Will create a requested number of supersets based on the following parameters:
        - number_of_supersets: number of supersets to exist WITHIN a SINGLE CIRCUIT
        - number_of_sets: number of sets to exist WITHIN a SINGLE SUPERSET
        """

        # base case
        if counter >= number_of_supersets: return
        
        # add the superset to the training plan JSON object
        supersetname = f"Superset {counter+1}"
        self.trainingplanjson["circuits"][-1]["supersets"].append({"superset_name":supersetname, "sets":[]})
        self.Sets(number_of_sets)
        
        # recursive call (counter is increased to trigger base case)
        counter += 1
        self.Supersets(number_of_supersets, number_of_sets, counter)

        
    def Circuits(self, number_of_circuits, number_of_supersets, number_of_sets):
        """
        Will create a requested number of circuits based on the following parameters:
        - number_of_circuits: number of circuits to exist in the training plan
        - number_of_supersets: number of supersets to exist WITHIN a SINGLE CIRCUIT
        - number_of_sets: number of sets to exist WITHIN a SINGLE SUPERSET
        """

        # base case
        if counter >= number_of_circuits: return

        # add the circuit title to the training plan JSON object
        circuitname = f"Circuit {counter+1}"
        self.trainingplanjson["circuits"].append({"circuit_name":circuitname, "supersets":[]})
        # call the Supersets function to add a specific number of supersets
        self.Supersets(number_of_supersets, number_of_sets)
        
        # recursive call (counter is increased to trigger base case)
        counter += 1
        self.Circuits(number_of_circuits, number_of_supersets, number_of_sets, counter = counter)




    def createtrainingplan(self, number_of_sets,number_of_circuits,number_of_supersets, planned_date=""):
        """
        Will create a training plan based on the following parameters:
        - number_of_circuits: number of circuits which will exist in the training plan
        - number_of_supersets: number of supersets which will exist in EACH circuit
        - number_of_sets: number of sets which will exist in EACH superset
        - planned_data: piece of metadata which refers to when the training session is to take place. (default None)
        """

        # error flag for if the user has selected more circuits/supersets/sets than the ExerciseData dataset has enough exercises to fill
        self.not_enough_exercises_error = False 
        # sets is used to record ALL exercises (sets) which have been added to the training plan so that no duplicates exist
        self.sets = []    

        # the Trainee (customer) has selected various goals (which correspond to Categories, and hence groups of exercises which they want to complete)
        # this loop will linear search through ALL POSSIBLE EXERCISES in the dataset, and include only those who have a link to the Categories stated in the customers goals (self.customer.goals)
        self.validexerciseIDs = []
        for exercise_id in self.master_controller.exercisedata_dict:
            exercise = self.master_controller.exercisedata_dict[exercise_id]
            if exercise.category in self.customer.goals:
                self.validexerciseIDs.append(exercise_id)
        

        trainingplan = TrainingPlan(self.master_controller, self.customer, number_of_circuits, number_of_supersets, number_of_sets, planned_date=planned_date)

        # initialising the JSON object with the core structure defined in the criteria
        #self.trainingplanjson = {"circuits":[],"warmup":[],"cooldown":[],"customerid":"", "timestamp":datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "planned_date": str(planned_date)}

        # begin generating the circuits using the Circuits method (note that this method will automatically branch off and call the Supersets and Sets methods)
        #self.Circuits(number_of_circuits,number_of_supersets,number_of_sets)


