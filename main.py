
from machine import Pin, I2C
import schedule
import time, utime
import ujson
from random import randint

import webServer
import sensors
import ssd1306

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


### Button setup
buttonInput = Pin(35, Pin.IN)
buttonInput.irq(trigger=Pin.IRQ_FALLING, handler=buttonJob)


# Complete project details at https://RandomNerdTutorials.com


webServer.webpageJob()

while True:
    schedule.run_pending()
    time.sleep(0.5)

