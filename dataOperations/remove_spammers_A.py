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

    #iterate through user responses

    responses = db.responses.find({'user': userName})

    ratings = []
    for item in responses:
        #check for batch and frame
        qType = str(item['type'])
        if qType == 'rating':
            batch = int(item['batch'])
            frame = int(item['frames'])
            ratString = item['estimates']  
            
            rat = []
            for i in ratString:
                rat.append(int(float(filter(lambda x: x.isdigit(), i))))

            # For A Test     
            #if any(x < 10 for x in rat) or any(x>170.05 for x in rat) or np.std(rat) > 36.82:
            #    print(rat, rat)

            # For B Test     
            if any(x < 2 for x in rat) or any(x>300 for x in rat) or np.std(rat) > 100.08:
                print(rat)
                bad = True

    if bad == True:
        usersRemove.append(userName)

print(usersRemove)

print("Users Removed: " + str(userRemoveCount))
