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

		ranking = []
		rating = []

		#get ground truth for specified question
		questionOrder = questions[i-1]

		rankResponse = responsesCol.find_one({"user": userName, "collection": str(i), "type": "ranking"})
		batch = int(rankResponse["batch"])
		frames = int(rankResponse["frames"])
        
		rank = rankResponse["ranking"]
		rankingTime = int(rankResponse["time"])

		ranking = [int(x) for x in rank]
		#Note: change rank to format
		pos = 1
		for ra in ranking:
			max_index = ranking.index(max(ranking))
			ranking[max_index] = pos
			pos += 1 

		#get pictures
		ratingTime = 0
		for j in range(frames):
			
			ratingResponse = responsesCol.find_one({"user": userName, "picture": str(j), "collection": str(i), "type": "rating"})
			ratingTimeIndividual = int(ratingResponse["time"])
			ratingResponse = ratingResponse["estimate"]
			ratingResponse = int(float(ratingResponse))
			
			rating.append(ratingResponse)
			ratingTime += ratingTimeIndividual

		#sort ratings in order of ground truth
		for k in range(1, len(questionOrder)):
			key = questionOrder[k] 
			key2 = rating[k]
			l = k-1

			while l>=0 and key < questionOrder[l]:
				questionOrder[l+1] = questionOrder[l]
				rating[l+1] = rating[l]
				l = l - 1
			rating[l+1] = key2
			questionOrder[l+1] = key
		
		question = {
			"batch": batch,
			"frames": frames,
 			"rankings": ranking,
			"ratings": rating,
			"groundtruth": questionOrder,
			"ratingTime": ratingTime,
			"rankingTime": rankingTime
		}

		dataArray.append(question)


rightNow = datetime.datetime.today().strftime('%m-%d-%Y')
file_name = rightNow + dbase + ".json" 

with open(str(file_name), 'w+') as outfile:
	json.dump(dataArray, outfile) 
