
from machine import Pin, Timer, I2C, SoftI2C
import ujson
from random import randint
import ahtx0

##### Sensor initialization

# setup pins for sensors
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
sensor = ahtx0.AHT10(i2c)

## setup timer for sensors
sensorCollectionTimer = Timer(0)
sensorCollectionTimer.init(period=5000, mode=Timer.PERIODIC, callback=sensorCollectionJob)

def sensorCollectionJob(sensorCollectionTimer):
    global sensor

    print ("Temperature:", sensor.temperature)
    print ("Humidity:", sensor.relative_humidity)
    data = {}
    
    data['temp'] = randint(15, 35)
    data['humid'] = randint(10, 90)
    data['height'] = randint(0, 100)

    writeSensorData(data)

def writeSensorData(dataDict):
    with open ('data.json' , 'r') as jsonFile:
        data = ujson.load(jsonFile)
        data['data'].append(dataDict)

    with open ('data.json', 'w') as jsonFile:
        ujson.dump(data, jsonFile)
