
from machine import Pin, I2C, unique_id, reset
import ubinascii
import schedule
import time, utime
import ujson
from random import randint
import network

#import sensors
import ssd1306
import simple



def connectWifi(ssid='CableBox-BF58', psk='ymn5gzm5um'):
    
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(ssid, psk)
    
    for a in range(10):
        if station.isconnected():
            print('Connection successful')
            print(station.ifconfig())
            return True
        
        time.sleep(1)

    return False

def blinkSequence(ledObject, blinks=1, onTime = 0.2, offTime = 0.25):
    if ledObject.value():
        ledObject.value(0)
        time.sleep(0.2)

    for a in range(blinks):
        ledObject.value(1)
        time.sleep(onTime)
        ledObject.value(0)
        time.sleep(offTime)

def buttonJob(buttonInput):
    if  not buttonInput.value():    # Button goes low on click, so if buttonInput == 0, means 'if button is clicked', prevents debouncing outputs on release
        print ("Button: ", buttonInput.value())



### Connect to the wifi
connectWifi()

### Button setup
buttonInput = Pin(35, Pin.IN)
buttonInput.irq(trigger=Pin.IRQ_FALLING, handler=buttonJob)


def callbackFunction(topic, msg):
    print ("Received subscriber message!", topic , "-", msg)

    ### If we received a command, handle it here:
    if topic == b'/command':
        if msg == b'ping':
            client.publish(b'/response', b'pong')

    ### If we received a setGraphInterval request, handle it here
    elif topic == b'/setGraphInterval':
        interval = int(msg)
        temp = {}

        with open ('data.json', 'r') as dataFile:
            temp = ujson.load(dataFile)

        data = {}
        temperature = []
        humidity = []
        height = []

        print ("Length of dataset:", len(temp['temperature']))
        print ("Interval is",interval)
        sampleLength = int(len(temp['temperature']))/interval

        print ("Samplelength: ", sampleLength)

        for b in range(0, len(temp['temperature']), interval):
            print ("b:",b)



        for a in range(20):
            temperature.append(temp['temperature'][-1-b])
            humidity.append(temp['humidity'][-1-b])
            height.append(temp['height'][-1-b])

        data['temperature'] = temperature[::-1]
        data['humidity'] = humidity[::-1]
        data['height'] = height[::-1]
        
        client.publish(b'/graphData', str(data).encode())
        print ("Published", data)

    else:
        print ("Received unhandled topic message", topic, msg)


def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  reset()


def mqttSetup():
    mqtt_server = '135.181.193.6'
    client_id = ubinascii.hexlify(unique_id())
    subscribeTopics = [ b'/command',
                        b'/setGraphInterval']

    client = simple.MQTTClient(client_id, mqtt_server)
    client.set_callback(callbackFunction)
    client.connect()
    for a in subscribeTopics:
        client.subscribe(a)
    print('Connected to %s MQTT broker' % (mqtt_server))
    return client


client = mqttSetup()


while True:
  try:
    client.check_msg()

  except OSError as e:
    restart_and_reconnect()
