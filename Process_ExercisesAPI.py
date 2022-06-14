import requests
import json
import tkinter as tk

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
    def __init__(self,id,name,description):
        self.id=id
        self.name=name
        self.description=description


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
        except requests.exceptions.RequestException as e:
            timeout += 1
            if timeout > 10: return excercises_objects



    for category in categories_json["results"]:
        category_dict[category["id"]]=ExerciseCategories(category["id"],category["name"])


    for category_id in category_dict:

        # link to retrieve the exercises for a specific category, category_id
        link = f"https://wger.de/api/v2/exercise/?category={category_id}&language=2"
        timeout = 0

        # link refers to the fetch link for the API. Seen as the database is so large, exercises are loaded in seperate "pages". In each page's data, it has a field "next" which links to the following page with exercises. This loop will continue to request exercises from all pages, until link becomes None (meanin the end case has been reached)
        while link != None: 
            try:
                #accessing API
                exercises_response = requests.get(link, headers=headers)
                exercises_json = json.loads(exercises_response.content.decode('utf-8'))

                # inserting the data retrieved for each exercise into an object
                for exercise in exercises_json["results"]:
                    exercise_obj = ExercisesAPI(exercise["id"],exercise["name"],exercise["description"])
                    # store the exercise object in a dictionary
                    excercises_objects[exercise["id"]]=exercise_obj
                
                # retrieve the next page to be loaded in the API
                link=exercises_json["next"]

            except requests.exceptions.RequestException as e:
                # try-catch will catch any errors thrown by the "requests" module. Note: this is done through the requests.exceptions.RequestException error which is the superclass for all requests errors (connection error/invalid response). Timeout will increment which means that a certain allowance will exist of any connection breaks before exiting the process
                timeout += 1
                
            except Exception as e:
                tk.messagebox.showerror(message="Invalid response from the API \n\n" + str(e))

            if timeout > 10: 
                return excercises_objects


    return excercises_objects
