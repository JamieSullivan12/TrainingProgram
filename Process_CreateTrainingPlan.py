from random import randint
import datetime
from tokenize import Triple
from tkinter import messagebox

from numpy import number



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
        # if there are not enough exercises left, an error will be thrown.
        # NOTE: this will be the case if there are not enough exercises in the database with the categories selected by the
        # trainer
        if len(self.validexerciseIDs) == 0:
            self.not_enough_exercises_error = True
            return

        if counter >= number_of_sets: return


        random_no = randint(0,len(self.validexerciseIDs)-1)
        exercise_obj = self.master_controller.exercisedata_dict[self.validexerciseIDs[random_no]]

        del self.validexerciseIDs[random_no]
        # some exercises will have the following methods of completion: (reps, time, distance)
        # for example:
        # - pushups is reps based (e.g., 10x pushups)
        # - plank is time based (e.g., 30s plank)
        # - sprinting is distance based (e.g., 100m sprint)
        reps="0"
        time="0" # seconds
        distance="0" # meters

        # the method of completion (reps, time distance) is defined by the "type" parameter in the Exercises database
        # NOTE: only the method of the selected exercise will be populated with a value. all others will be 0
        if exercise_obj.type==1 or exercise_obj.type==2:
            reps=str(self.round(10*self.customer.ability_level,base=5))
        elif exercise_obj.type==3 or exercise_obj.type==4:
            time=str(self.round(20*self.customer.ability_level, base=5))
        elif exercise_obj.type==5:
            distance=str(self.round(25*self.customer.ability_level,base=5))

        self.trainingplanjson["circuits"][-1]["supersets"][-1]["sets"].append({"exercise_id":str(exercise_obj.ID), "name": exercise_obj.descriptor, "reps":str(reps),"time":str(time),"distance":str(distance)})

        counter += 1
        self.Sets(number_of_sets, counter)

    def Supersets(self, number_of_supersets, number_of_sets, counter = 0):
        """
        Will create a requested number of supersets based on the following parameters:
        - number_of_supersets: number of supersets to exist WITHIN a SINGLE CIRCUIT
        - number_of_sets: number of sets to exist WITHIN a SINGLE SUPERSET
        """

        if counter >= number_of_supersets: return
        
        # add the superset to the training plan JSON object
        supersetname = f"Superset {counter+1}"

        self.trainingplanjson["circuits"][-1]["supersets"].append({"superset_name":supersetname, "sets":[]})
        self.Sets(number_of_sets)
        
        counter += 1
        self.Supersets(number_of_supersets, number_of_sets, counter)

        
    def Circuits(self, number_of_circuits, number_of_supersets, number_of_sets, counter = 0):
        """
        Will create a requested number of circuits based on the following parameters:
        - number_of_circuits: number of circuits to exist in the training plan
        - number_of_supersets: number of supersets to exist WITHIN a SINGLE CIRCUIT
        - number_of_sets: number of sets to exist WITHIN a SINGLE SUPERSET
        """
        if counter >= number_of_circuits: return

        # add the circuit title to the training plan JSON object
        circuitname = f"Circuit {counter+1}"
        self.trainingplanjson["circuits"].append({"circuit_name":circuitname, "supersets":[]})
        # call the Supersets function to add a specific number of supersets
        self.Supersets(number_of_supersets, number_of_sets)

        counter += 1
        self.Circuits(number_of_circuits, number_of_supersets, number_of_sets, counter = counter)




    def createtrainingplan(self, number_of_sets,number_of_circuits,number_of_supersets, planned_date=None):
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
        
        # initialising the JSON object with the core structure defined in the criteria
        self.trainingplanjson = {"circuits":[],"warmup":[],"cooldown":[],"customerid":"", "timestamp":datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "planned_date": str(planned_date)}

        # begin generating the circuits using the Circuits method (note that this method will automatically branch off and call the Supersets and Sets methods)
        self.Circuits(number_of_circuits,number_of_supersets,number_of_sets)

        if self.not_enough_exercises_error == True:
            result = messagebox.askyesno(title="WARNING", message="There are not enough exercises to fill the requested training plan structure\n\nPlease either select more goals or decrease training plan size.\n\nWould you like to ignore this message?")
            if result == True:
                # add the session plan to the customer's session plans list (in the customer object)
                self.customer.training_plans.append(self.trainingplanjson)
                # save changes
                self.customer.writetofile()
        
