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

#response = requests.get("https://wger.de/api/v2/workout/")
url = 'http://api/v2/exercise/?muscles=1&equipment=3'
headers = {'Accept': 'application/json','Authorization': 'Token 8b33edb3c3f6921d2e3f099cdb9a9fa190570721',"language":"en"}

categories = {}
exercise_categories_response = requests.get("https://wger.de/api/v2/exercisecategory", headers=headers)
categories_json =json.loads(exercise_categories_response.content)['results']
print("loading categories")
for category in categories_json:
    
    categories[category["id"]]=ExerciseCategories(category["id"],category["name"])
print("loading exercise database")
g=1 # category counter
for category_id in categories:
    i=20 # exercise page counter
    link = f"https://wger.de/api/v2/exercise/?category={category_id}&language=2"
    while link != None:
        exercises_response = requests.get(link, headers=headers)
        exercises_json =json.loads(exercises_response.content)
        link=exercises_json["next"]
        
        # used to display status message
        if i > exercises_json["count"]:i=exercises_json["count"]
        perc=round((i/exercises_json["count"])*100,2)
        print(f"({g}/{len(categories)}) loading exercises for category {categories[category_id].name} {perc}%")
        i += 20

        for exercise in exercises_json["results"]:
            exc = Exercises(exercise["id"],exercise["name"],exercise["description"],categories[exercise["category"]],exercise["equipment"])
            categories[category_id].add_exercise(exc)
    g+=1
