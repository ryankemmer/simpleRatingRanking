import pymongo
import json
import sys
import numpy as np
import datetime

url = 'mongodb://localhost:27017/'  

dbase = sys.argv[1]
print(dbase)

client = pymongo.MongoClient(url)
db = client[dbase]
usersCol = db['users']
responsesCol = db['responses']
batchesCol = db['batches']

usersArray = []

for user in usersCol.find():
    surveyResults = user['surveyResults']
    usersArray.append(surveyResults)

rightNow = datetime.datetime.today().strftime('%m-%d-%Y')
file_name = 'DEMOGRAPHICS' + rightNow + dbase + ".json" 

with open(str(file_name), 'w+') as outfile:
	json.dump(usersArray, outfile) 
