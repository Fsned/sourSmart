from random import randint
import datetime
from json import dump

# Initiate empty json list to contain all datasets
data = []

for a in range(12):

    dataSet = {}
    #dataSet['time'] = str(datetime.datetime.now().time())
    dataSet['temp'] = randint(20, 30)
    dataSet['humid'] = randint(25, 90)
    dataSet['height'] = randint(0, 100)

    data.append(dataSet)
        
with open ('testData.json', 'w') as f:
    dump(data, f)

print ("Generated", data.__len__() , "datasets")