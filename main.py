
from machine import Pin, Timer
import schedule
import time, utime
import ujson
from random import randint

import webServer

usingSensors = False
startWebServer = True

sensorCollectionTimer = Timer(0)




def blinkSequence(blinks=1, onTime = 0.2, offTime = 0.25):
    if led.value():
        led.value(0)
        time.sleep(0.2)

    for a in range(blinks):
        led.value(1)
        time.sleep(onTime)
        led.value(0)
        time.sleep(offTime)

def aliveJob():
    print ("I'm alive")

def buttonJob(buttonInput):
    if  not buttonInput.value():    # Button goes low on click, so if buttonInput == 0, means 'if button is clicked', prevents debouncing outputs on release
        print ("Button: ", buttonInput.value())

def writeSensorData(dataPoint, filename):
    currDate = time.localtime()
    currTime = time.localtime()

    #print (utime.localtime())
    #print ("currDate: ", currDate)
    #print ("currTime: ", currTime)

#    with open filename as file:

def sensorCollectionJob(sensorCollectionTimer):    
    if usingSensors == True:
        print ("Sensorstuff should go here!")
        # Temperature data


        # Humidity data


        # Height of dough data



    else:
        # Generate random data
        temp = randint(15, 35)
        humid = randint(10, 90)
        height = randint(0, 100)

        writeSensorData(temp, 'temps.json')
        writeSensorData(humid, 'humid.json')
        writeSensorData(height, 'height.json')


### Button setup
buttonInput = Pin(35, Pin.IN)
buttonInput.irq(trigger=Pin.IRQ_FALLING, handler=buttonJob)


### Webpage setup


### SensorCollection timer setup
sensorCollectionTimer.init(period=5000, mode=Timer.PERIODIC, callback=sensorCollectionJob)


# Complete project details at https://RandomNerdTutorials.com


webServer.webpageJob()

while True:
    schedule.run_pending()
    time.sleep(0.5)

