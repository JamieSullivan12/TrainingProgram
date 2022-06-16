import random
import datetime
from tokenize import Triple
from tkinter import messagebox


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

        def __init__(self, parent_controller, exercisedataset, import_data=""):
            """
            Will create a set. All functions required to generate a set are completed in this class:
            - randomly selecting a set from the list of available exercises (parameter exercisedataset)
            - calculating the duration of the set (based on the set type and trainee ability level)
            NOTE: import_data can be passed in case an existing set needs to be read into this class. The
                set must be in the format {ID:String, Length:String, OverrideName:String, OverrideLength:String}.
            """

            self.parent_controller=parent_controller

            # the length/duration of a set can take on three types:
            self.reps=0 # repetitions
            self.time=0 # seconds
            self.distance=0 # meters

            # if a customer has manually edited the set, these values will override those orginally defined
            self.overridelength = "0"
            self.overridename = ""

            # if override_data != "" means that the function IS being used to import an already generated class
            # this means that instead of randomly choosing a set from the ExerciseData class, the already defined
            # exercise ID needs to be linked as an aggregation relationship with the ExerciseData class
            changelength=""
            if import_data != "":
                if import_data["OverrideName"] != "": self.overridename = import_data["OverrideName"]
                if import_data["OverrideLength"] != "": self.overridelength = import_data["OverrideLength"]
                # search for a link between the ID of the imported exercise and the class ExerciseData
                for exercise_id in self.parent_controller.master_controller.exercisedata_dict:
                    exercise = self.parent_controller.master_controller.exercisedata_dict[exercise_id]
                    if str(int(exercise.ID)) == import_data["ID"]:
                        self.exercise_obj = exercise
                changelength = import_data["Length"]

            else:
                # check if there are enough exercises left in the database to fill the requested number of circuits/stations/sets.
                if len(exercisedataset) <= parent_controller.total_number_of_exercises:
                    parent_controller.not_enough_exercises_error = True
                    return

                # choose a random exercise from the available selection of ExerciseData objects (using randint library)
                self.exercise_obj=random.choice(list(self.parent_controller.master_controller.exercisedata_dict.values()))
                #random_no = randint(0,len(exercisedataset)-1)
                #self.exercise_obj = self.parent_controller.master_controller.exercisedata_dict[exercisedataset[random_no]]

            # calculate the duration of each set (based on the type of exercise and customer ability level)
            # NOTE that the first if statement makes sure to ignore the following block of code if the funciton is being run as
            # an import function.
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

    class Station():
        def __init__(self, parent_controller, exercisedataset, import_data = ""):
            # store an aggregation of sets within each station object
            self.sets = []

            if import_data == "":
              # create a certain number of sets (by instantiating the Sett() class and storing them in an array, here)
                count = 0
                while count < parent_controller.number_of_sets:
                    self.sets.append(parent_controller.Set(parent_controller, exercisedataset))
                    count = count + 1
            
            else:
                for set in import_data["sets"]:
                    self.sets.append(parent_controller.Set(parent_controller, exercisedataset, import_data=set))

    class Circuit():
        def __init__(self, parent_controller, exercisedataset, import_data = ""):
            # store the aggregation of stations for each circuit object
            self.stations = []

            # if there is no import data, a training plan needs to be GENERATED (instantiating the Station class)
            if import_data == "":
                count = 0
                while count < parent_controller.number_of_stations:
                    self.stations.append(parent_controller.Station(parent_controller, exercisedataset))
                    count = count + 1


            else:
                print(import_data)
                for station in import_data["stations"]:
                    self.stations.append(parent_controller.Station(parent_controller, exercisedataset, import_data=station))
            

    def generate_training_plan(self, number_of_sets, number_of_stations, number_of_circuits,):

        self.number_of_sets = number_of_sets
        self.number_of_stations = number_of_stations
        self.number_of_circuits = number_of_circuits

        self.total_number_of_exercises = 0

        for exercise_id in self.master_controller.exercisedata_dict:
            exercise = self.master_controller.exercisedata_dict[exercise_id]

            if exercise.category in self.traineeobj.goals:
                self.validexerciseIDs.append(exercise_id)

        count = 0
        # instantiate the required number of Circuit objects (loop count from 0 to self.number_of_circuits)
        # and store in a list of circuits (attributed to the TrainingPlan class)
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
            self.exportstring["circuits"].append({"stations":[]})
            for super_count, station in enumerate(circuit.stations):
                self.exportstring["circuits"][circ_count]["stations"].append({"sets":[]})
                for set_count, set in enumerate(station.sets):
                    self.exportstring["circuits"][circ_count]["stations"][super_count]["sets"].append({})
                    self.exportstring["circuits"][circ_count]["stations"][super_count]["sets"][set_count] = {
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
            self.circuits.append(self.Circuit(self, exercisedataset = self.master_controller.exercisedata_dict, import_data=circuit))
        self.export_to_string()
