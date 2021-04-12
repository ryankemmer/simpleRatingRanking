import numpy as np
import json

with open('08-21-2020ratingsrankingsB1.json') as json_file:
    data = json.load(json_file)

for item in data:
    #check for batch and frame
    batch = int(item['batch'])
    frame = int(item['frames'])
    ran = item['rankings']
    rat = item['ratings']  

    # For A Test     
    #if any(x < 10 for x in rat) or any(x>170.05 for x in rat) or np.std(rat) > 36.82:
    #    print(rat, rat)

    # For A Test     
    if any(x < 2 for x in rat) or any(x>300 for x in rat) or np.std(rat) > 100.08:
        print(rat, rat)