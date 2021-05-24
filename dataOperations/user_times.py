import pymongo
import json
import time
import datetime
import sys

#url = 'mongodb://10.218.105.218:27017/'
url = 'mongodb://localhost:27017/'

dbase = sys.argv[1]

#set up database and all columns 
client = pymongo.MongoClient(url)
db = client[dbase]
usersCol = db['users']
responsesCol = db['responses']

dataArray = []

#iterate over users
for user in usersCol.find():

	#get username
	userName = user['user']
	print(userName)
	#get questions
	questions = user['questions']

	#get the users responses for each question 
	for i in range(1,5):

        	#find rank
		rankResponse = responsesCol.find_one({"user": userName, "collection": str(i), "type": "ranking"})
        	ranktime = int(rankResponse["time"])
       		frames = int(rankResponse["frames"])

		#get pictures

        	ratingtime = 0
        	for j in range(frames):
			
			ratingResponse = responsesCol.find_one({"user": userName, "picture": str(j), "collection": str(i), "type": "rating"})
			time = int(ratingResponse["time"])
			ratingtime += time
		
        	question = {
            		"user": userName,
			"frames": frames,
 			"rankingTime": ranktime,
			"ratingTime": ratingtime,
		}

        	dataArray.append(question)


file_name = "times" + dbase + ".json" 

with open(str(file_name), 'w+') as outfile:
	json.dump(dataArray, outfile) 