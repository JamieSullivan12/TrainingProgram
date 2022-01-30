from random import randint

class TrainingPlanCreator():
    
    class Rep():
        def __init__(self,exercise_obj):
            self.exercise_obj=exercise_obj
            # a variable which when toggled, will isntruct the user to complete the exercise on both arms/legs.
            # will only be toggled if the "type" description is that of an exercise where this is required (see descriptions
            # below)
            self.eachside=False 

            self.repeat=0
            self.time=0 # seconds
            self.distance=0 # meters

            # a type of exercise which is rep-based
            if self.exercise_obj.type==1:
                self.repeat=10
            # a type of exercise which is rep-based and needs to be repeated for the other arm/leg
            if self.exercise_obj.type==2:
                self.repeat=20
                self.eachside=True
            # a type of exercise which is time based
            if self.exercise_obj.type==3:
                self.time=45
            # a type of exercise which is time based, and needs to be repeated for the other arm/leg
            if self.exercise_obj.type==4:
                self.time=30
                self.eachside=True
            # a type of exercise which is distance based
            if self.exercise_obj.type==5:
                self.distance=50
            


    def __init__(self, customer, master_controller):
        self.customer=customer
        self.master_controller=master_controller
    
    def createtrainingplan(self):
        self.validexerciseIDs = []
        for exercise_id in self.master_controller.exercisedata_dict:
            exercise = self.master_controller.exercisedata_dict[exercise_id]
            if exercise.category in self.customer.categories:
                self.validexerciseIDs.append(exercise_id)
        
        reps=[]
        for i in range(4):
            random_no = randint(0,len(self.validexerciseIDs)-1)
            rep=self.Rep(self.master_controller.exercisedata_dict[self.validexerciseIDs[random_no]])
            reps.append(rep)
        
        for rep in reps:
            print (rep.exercise_obj.descriptor, rep.time, rep.repeat, rep.distance, rep.eachside)
        print()
