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

class Exercises():
    def __init__(self,id,name,description,category,equiptment):
        self.id=id
        self.name=name
        self.description=description
        self.category=category
        self.equiptment=equiptment


def load_data():
    load_local=True
    headers = {'Accept': 'application/json','Authorization': 'Token 8b33edb3c3f6921d2e3f099cdb9a9fa190570721',"language":"en"}

    #getting the exercise categories using the API
    category_dict = {}
    if not load_local:
        category_file = open("categories.json","w")
        exercise_categories_response = requests.get("https://wger.de/api/v2/exercisecategory", headers=headers)
        categories_json =json.loads(exercise_categories_response.content)
        json.dump(categories_json, category_file)
        category_file.close()
    else:
        category_file = open("categories.json")
        categories_json =json.load(category_file)


    print("loading categories")
    for category in categories_json["results"]:
        category_dict[category["id"]]=ExerciseCategories(category["id"],category["name"])

    print(category_dict)
    exercise_dict = {}

    # locally sourcing the data from a file
    if load_local:
        print("loading exercise database: LOCAL")
        exercises_file = open("exercises.json","r")
        exercises_json=json.load(exercises_file)
        for page in exercises_json:
            for exercise in page["results"]:
                exc = Exercises(exercise["id"],exercise["name"],exercise["description"],category_dict[exercise["category"]],exercise["equipment"])
                exercise_dict[exc.id]=exc
                category_dict[exc.category.id].add_exercise(exc)

    else:
        print("loading exercise database: ONLINE")
        f = open("exercises.json","w")

        exercises_json_list=[]
        for category_id in category_dict:
            link = f"https://wger.de/api/v2/exercise/?category={category_id}&language=2"
            while link != None: #link becomes None when no more pages are available to be loaded
                #accessing API
                exercises_response = requests.get(link, headers=headers)
                exercises_json =json.loads(exercises_response.content)
                exercises_json_list.append(exercises_json)
                
                link=exercises_json["next"]

                # converting data into a class
                for exercise in exercises_json["results"]:
                    exc = Exercises(exercise["id"],exercise["name"],exercise["description"],category_dict[exercise["category"]],exercise["equipment"])
                    category_dict[category_id].add_exercise(exc)

        # writing the data to a local file so it can be used in the future
        json.dump(exercises_json_list,f)
