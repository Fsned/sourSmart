from random import randint
import datetime
from json import dump

# Initiate empty json list to contain all datasets
temperature = []
humidity = []
height = []

data = {}
for a in range(29):
    temperature.append(randint(20, 30))
    humidity.append(randint(25, 90))
    height.append(randint(0, 100))

data['temperature'] = temperature
data['humidity'] = humidity
data['height'] = height

with open ('data.json', 'w') as f:
    dump(data, f)

print ("Generated", data.__len__() , "datasets")