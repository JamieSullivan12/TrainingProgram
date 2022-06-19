import random
import datetime


class TrainingPlan():

    def __init__(self, mainline_obj, traineeobj, planned_date = ""):
        # assigning attributes specific to this training plan
        self.__traineeobj = traineeobj
        self.__circuits = []
        self.__timestamp = str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        self.__planned_date = planned_date
        self.__mainline_obj=mainline_obj
        self.__not_enough_exercises_error=False

    class Set():
        def round(self,x, base=5):
            return base * round(x/base)

        def __init__(self, parent_controller, import_data=""):
            """
            Will create a set. All functions required to generate a set are completed in this class:
            - randomly selecting a set from the list of available exercises (parameter exercisedataset)
            - calculating the duration of the set (based on the set format and trainee ability level)
            NOTE: import_data can be passed in case an existing set needs to be read into this class. The
                set must be in the format {ID:String, Length:String, OverrideName:String, OverrideLength:String}.
            """

            self.parent_controller=parent_controller

            # the length/duration of a set:
            self.length = 0

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
                for exercise_id in self.parent_controller.mainline_obj.exercisedata_dict:
                    exercise = self.parent_controller.mainline_obj.exercisedata_dict[exercise_id]
                    if str(int(exercise.ID)) == import_data["ID"]:
                        self.exercise_obj = exercise
                changelength = import_data["Length"]

            else:


                # choose a random exercise from the available selection of ExerciseData objects (using randint library)
                
                if len(self.parent_controller.validexerciseIDs) == 0:
                    parent_controller.not_enough_exercises_error = True
                    return
                else:
                    self.exercise_obj=random.choice(list(self.parent_controller.validexerciseIDs.values()))
                    self.parent_controller.validexerciseIDs.pop(self.exercise_obj.ID,None)


            # calculate the duration of each set (based on the format of exercise and customer ability level)
            # NOTE that the first if statement makes sure to ignore the following block of code if the funciton is being run as
            if str(self.overridelength) != 0 and str(self.overridelength) != "" and str(self.overridelength) != None:
                if self.exercise_obj.format==1:
                    self.length=str(self.round(10*self.parent_controller.traineeobj.ability_level,base=5))
                    if changelength != "": self.length=changelength
                elif self.exercise_obj.format==2:
                    self.length=str(self.round(20*self.parent_controller.traineeobj.ability_level, base=5))
                    if changelength != "": self.length=changelength
                elif self.exercise_obj.format==3:
                    self.length=str(self.round(25*self.parent_controller.traineeobj.ability_level,base=5))
                    if changelength != "": self.length=changelength
                elif self.exercise_obj.format == 4:
                    self.length=str(self.round(150*self.parent_controller.traineeobj.ability_level,base=100))
                if changelength != "": self.length=changelength

        def getexerciselength(self):
            return self.length

    class Station():
        def __init__(self, parent_controller, import_data = ""):
            # store an aggregation of sets within each station object
            self.sets = []
            # if there is no import data, a training plan needs to be GENERATED
            if import_data == "":
                count = 0
                while count < parent_controller.number_of_sets:
                    self.sets.append(parent_controller.Set(parent_controller))
                    count = count + 1
            
            else:
                for set in import_data["sets"]:
                    self.sets.append(parent_controller.Set(parent_controller, import_data=set))

    class Circuit():
        def __init__(self, parent_controller, import_data = ""):
            # store the aggregation of stations for each circuit object
            self.stations = []
            # if there is no import data, a training plan needs to be GENERATED
            if import_data == "":
                count = 0
                while count < parent_controller.number_of_stations:
                    self.stations.append(parent_controller.Station(parent_controller))
                    count = count + 1


            else:
                for station in import_data["stations"]:
                    self.stations.append(parent_controller.Station(parent_controller, import_data=station))
            
    def generate_training_plan(self, number_of_sets, number_of_stations, number_of_circuits,):

        self.__number_of_sets = number_of_sets
        self.__number_of_stations = number_of_stations
        self.__number_of_circuits = number_of_circuits

        self.total_number_of_exercises = 0

        self.__validexerciseIDs={}
        for exercise_id in self.__mainline_obj.exercisedata_dict:
            exercise = self.__mainline_obj.exercisedata_dict[exercise_id]
            if exercise.category in self.__traineeobj.goals:
                self.__validexerciseIDs[exercise_id]=exercise

        count = 0
        # instantiate the required number of Circuit objects (loop count from 0 to self.number_of_circuits)
        # and store in a list of circuits (attributed to the TrainingPlan class)
        while count < self.__number_of_circuits:
            self.__circuits.append(self.Circuit(self))
            count = count + 1

        if self.__not_enough_exercises_error == True:
            return
        
        self.add_to_trainee()
    

    def add_to_trainee(self):
        self.__traineeobj.training_plans.append(self)

    def export_to_string(self):
        """
        Function will export the circuits/stations/sets structure to be compatible with permenant storage
        """

        self.exportstring = {"circuits":[],"customerid":str(self.__traineeobj.ID), "timestamp":str(self.__timestamp), "planned_date": str(self.__planned_date)}

        for circ_count, circuit in enumerate(self.__circuits):
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
        """
        Function will create the circuits/stations/sets structure when given a string from permenant storage
        """
        self.importstring = importstring
        self.__timestamp = importstring["timestamp"]
        self.__planned_date = importstring["planned_date"]
        for circuit in self.importstring["circuits"]:
            self.__circuits.append(self.Circuit(self, import_data=circuit))
        self.export_to_string()


    # GETTERS AND SETTERS
    @property
    def not_enough_exercises_error(self):
        return self.__not_enough_exercises_error

    @property
    def validexerciseIDs(self):
        return self.__validexerciseIDs

    @property
    def mainline_obj(self):
        return self.__mainline_obj
    
    @property
    def timestamp(self):
        return self.__timestamp
    
    @property
    def number_of_circuits(self):
        return self.__number_of_circuits

    @property
    def number_of_stations(self):
        return self.__number_of_stations
    
    @property
    def circuits(self):
        return self.__circuits

    @property
    def number_of_sets(self):
        return self.__number_of_sets
    

    @property
    def planned_date(self):
        return self.__planned_date

    @property
    def traineeobj(self):
        return self.__traineeobj
    
    @not_enough_exercises_error.setter
    def not_enough_exercises_error(self, var):
        """
        Setter method for not_enough_exercises_error (if var is not bool then it will default to True)
        """
        if var == True or var == False:
            self.__not_enough_exercises_error = var
        else:
            self.__not_enough_exercises_error = True
