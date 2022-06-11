from pickle import FALSE
import requests
import json
from pprint import pprint

class ExerciseCategories():
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.exercises = []
    
    def get_name(self):
        return self.name
    
    def add_exercise(self,exercise_obj):
        self.exercises.append(exercise_obj)

class ExercisesAPI():
    def __init__(self,id,name,description,category,equiptment):
        self.id=id
        self.name=name
        self.description=description
        self.category=category
        self.equiptment=equiptment


def load_data():
    headers = {'Accept': 'application/json','Authorization': 'Token 8b33edb3c3f6921d2e3f099cdb9a9fa190570721',"language":"en"}

    #getting the exercise categories using the API
    category_dict = {}
    excercises_objects = {}
    cont = False
    timeout = 0

    while cont == False:
        try:
            exercise_categories_response = requests.get("https://wger.de/api/v2/exercisecategory", headers=headers)
            categories_json =json.loads(exercise_categories_response.content)
            cont = True
            #json.dump(categories_json, category_file)
            #category_file.close()
        except Exception as e:
            timeout += 1
            if timeout > 10: return excercises_objects



    print("loading categories")
    for category in categories_json["results"]:
        category_dict[category["id"]]=ExerciseCategories(category["id"],category["name"])

    print(category_dict)
    print("loading exercise database: ONLINE")
    #f = open("exercises.json","w")

    
    count = 0
    exercises_json_list=[]
    for category_id in category_dict:
        print("fdjgn")
        link = f"https://wger.de/api/v2/exercise/?category={category_id}&language=2"
        timeout = 0
        
        while link != None: #link becomes None when no more pages are available to be loaded
            print("loading")
            #accessing API
            try:
                exercises_response = requests.get(link, headers=headers)
                #print(exercise_categories_response.status_code)
                #print(exercises_response.content)
                exercises_json = json.loads(exercises_response.content.decode('utf-8'))
                exercises_json_list.append(exercises_json)
                link=exercises_json["next"]
                # converting data into a class
                for exercise in exercises_json["results"]:
                    exc = ExercisesAPI(exercise["id"],exercise["name"],exercise["description"],category_dict[exercise["category"]],exercise["equipment"])
                    category_dict[category_id].add_exercise(exc)
                    excercises_objects[exercise["id"]]=exc
            except Exception as e:
                print("I got here")
                timeout += 1
            if timeout > 10: return excercises_objects

        if count > 0: return excercises_objects
        count += 1

                


    
    for ex in excercises_objects:
        print(excercises_objects[ex].name)
    # writing the data to a local file so it can be used in the future
    #json.dump(exercises_json_list,f)
    return excercises_objects
