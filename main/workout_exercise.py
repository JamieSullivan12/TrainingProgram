import requests
import json
from pprint import pprint
#response = requests.get("https://wger.de/api/v2/workout/")
url = 'http://api/v2/exercise/?muscles=1&equipment=3'
headers = {'Accept': 'application/json','Authorization': 'Token 8b33edb3c3f6921d2e3f099cdb9a9fa190570721',"language":"en"}
params = '{"language":2,"equipment":[1,3,4,5,7,10]}'
response = requests.get("https://wger.de/api/v2/exercise/?language=2&muscles=1&equipment=3", params=params, headers=headers)

#print(json.loads(response.content))
#r = requests.patch(url=url, data=data, headers=headers)
#print(json.loads(response.content)["results"])
exercises =json.loads(response.content)['results']
#print(exercises)
#print(response.content)
#data = json.load(json.loads(response.content)["results"])

for exercise in exercises:
    print(exercise["name"])
    print(exercise["language"])