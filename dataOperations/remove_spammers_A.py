import pymongo
import json
import sys
import numpy as np

url = 'mongodb://localhost:27017/'  

dbase = sys.argv[1]
print(dbase)

client = pymongo.MongoClient(url)
db = client[dbase]
usersCol = db['users']
responsesCol = db['responses']
batchesCol = db['batches']

args = len(sys.argv) - 1

userRemoveCount = 0
usersRemove = []

#Step 1: get bad users
for user in usersCol.find():

    bad = False

    key2pay = user["key2pay"]
    userName = user["user"]
    indexes = user["indexes"]
    questions = user['questions']

    #get the users responses for each question 
    for i in range(1,5):
        ranking = []
        rat = []

        rankResponse = responsesCol.find_one({"user": userName, "collection": str(i), "type": "ranking"})
        batch = int(rankResponse["batch"])
        frames = int(rankResponse["frames"])

		#get pictures
        for j in range(frames):
			
            ratingResponse = responsesCol.find_one({"user": userName, "picture": str(j), "collection": str(i), "type": "rating"})
            ratingResponse = ratingResponse["estimate"]
            ratingResponse = int(float(ratingResponse))
            rat.append(ratingResponse)
		
        #For A Test     
        if any(x < 10 for x in rat) or any(x>170.05 for x in rat) or np.std(rat) > 36.82:
            print(rat)
            bad = True

    if bad == True:
        usersRemove.append(userName)

print(usersRemove)

print("Users Removed: " + str(userRemoveCount))
