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

#Step 2: delete bad users
if(args > 1):
    if(sys.argv[2] == "delete"):

        for user in usersRemove:
            remUser = usersCol.find({'user' : user})

            userName_rem = remUser['user']
            indexes_rem = remUser['indexes']

            #remove assignment from batch 
            for i in range(len(indexes_rem)):
            
                question = str(indexes_rem[i][2])
                update = {"$set": {}}
                update['$set']["assignmentStatus."+question] = 0
        
                batchesCol.update_one({'size': indexes_rem[i][0], 'number': indexes_rem[i][1]}, update)
                        
                responsesCol.delete_many({'user' : userName})
                usersCol.delete_one({'user' : userName})
        
                userRemoveCount+=1


print("Users Removed: " + str(userRemoveCount))
