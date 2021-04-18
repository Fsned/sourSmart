from machine import Pin, Timer, SoftI2C
import ujson
from random import randint
import ahtx0
from utime import sleep
import VL5XLX

##### Sensor initialization
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))

envSensor = None
tofSensor = None

## Setup power-pins for the 2 sensors
envSensorPower = Pin(12, Pin.OUT)
tofSensorPower = Pin(13, Pin.OUT)

## Zero both powers
envSensorPower.value(0)
tofSensorPower.value(0)

## Init setup of env sensor
try:
    print ("Setting up envSensor...")
    envSensorPower.value(1)
    sleep(0.5)
    envSensor = ahtx0.AHT10(i2c)
    print ("envSensor setup success!")

except:
    print ("Failed setting up envSensor")
    envSensorPower.value(0)
    
try:
    print ("Setting up ToF Sensor...")
    tofSensorPower.value(1)
    sleep(0.5)
    tofSensor = VL5XLX.VL53L1X(i2c)
    envSensorPower.value(1)
    print ("ToF Sensor setup success!")
except:
    print("Failed setting up ToFSensor")
    tofSensorPower.value(0)
    print (tofSensor)

def sensorCollectionJob():
    
    data = {}
    if envSensor != None:
        data['temperature'] = envSensor.temperature
        data['humidity'] = envSensor.relative_humidity

    else:
        data['temperature'] = randint(15, 35)
        data['humidity'] = randint(10, 90)
    
    if tofSensor != None:
        data['height'] = (int(tofSensor.read()) / 10)
    else:
        data['height'] = randint(0, 100)

    writeSensorData(data)

def writeSensorData(dataDict):
    with open ('data.json' , 'r') as jsonFile:
        data = ujson.load(jsonFile)
        
        ### If there's >= 80 datapoints, delete the oldest ones
    if len(data['temperature']) >= 80:
        dataOverflowAmount = len(data['temperature']) - 79

        print ("Deleting", dataOverflowAmount, "datapoints")

        for a in range(dataOverflowAmount):
            del data['temperature'][0]
            del data['humidity'][0]
            del data['height'][0]

    data['temperature'].append(dataDict['temperature'])
    data['humidity'].append(dataDict['humidity'])
    data['height'].append(dataDict['height'])

    with open ('data.json', 'w') as jsonFile:
        ujson.dump(data, jsonFile)


def printDataLib():
    with open ('data.json', 'r') as jsonFile:
        data = ujson.load(jsonFile)
        for a in data:
            print (a, data[a])


def deleteData():
    with open('data.json', 'w') as jsonFile:
        data = {}
        
        data['temperature'] = []
        data['humidity'] = []
        data['height'] = []

        ujson.dump(data, jsonFile)
