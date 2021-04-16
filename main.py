
from machine import Pin, I2C, reset
from machine import deepsleep
import schedule
import utime
from time import sleep
import ujson
from random import randint
import utils
import ubinascii        # Used by the MQTT setup
import simple           # Used by MQTT
from machine import unique_id
import esp32

#import sensors
import ssd1306


def callbackFunction(topic, msg):
    msg = msg.decode('utf-8')
    topic = topic.decode('utf-8')

    print ("Received:", msg, "on topic:", topic)
    ### If we received a command, handle it here:
    if topic == '/command':
        if msg == 'ping':
            client.publish(b'/response', b'pong')
        
        elif msg == 'restart':
            client.publish(b'/response', b'restarting in 5...')
            sleep(5)
            reset()


    ### If we received a setGraphInterval request, handle it here
    elif topic == '/setGraphInterval':
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
            temperature.append(temp['temperature'][-1-(interval*a)])
            humidity.append(temp['humidity'][-1-(interval*a)])
            height.append(temp['height'][-1-(interval*a)])

        data['temperature'] = temperature[::-1]
        data['humidity'] = humidity[::-1]
        data['height'] = height[::-1]
        
        client.publish(b'/graphData', str(data).encode())
        print ("Published", data)

    elif topic == '/toggleFeed':
        temp = {}

        with open ('data.json', 'r') as dataFile:
            temp = ujson.load(dataFile)

        response = {}
        response['time'] = msg
        response['currentHeight'] = temp['height'][-1]

        client.publish(b'/feedData', str(response).encode())
        
    else:
        print ("Received unhandled topic message", topic, msg)



def buttonJob(buttonInput):
    global timer

    if  not buttonInput.value():    # Button goes low on click, so if buttonInput == 0, means 'if button is clicked', prevents debouncing outputs on release
        timer += 60 # add seconds to the timer...
        print ("New timer:", timer)




### Button setup
buttonInput = Pin(35, Pin.IN)
buttonInput.irq(trigger=Pin.IRQ_FALLING, handler=buttonJob)
esp32.wake_on_ext0(pin = buttonInput, level = esp32.WAKEUP_ANY_HIGH)


def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  sleep(10)
  reset()


def mqttSetup():
    mqtt_server = '135.181.193.6'
    client_id = ubinascii.hexlify(unique_id())
    subscribeTopics = [ b'/command',
                        b'/setGraphInterval',
                        b'/toggleFeed']

    client = simple.MQTTClient(client_id, mqtt_server)
    client.set_callback(callbackFunction)
    client.connect()
    for a in subscribeTopics:
        client.subscribe(a)

    print('Connected to %s MQTT broker' % (mqtt_server))
    return client


def goToSleep(minutes=1):
    client.publish(b'/response',b'Sleeping for', minutes, 'minutes')
    sleep(1)
    deepsleep(minutes*60*1000)





### Bootup
utils.connectWifi('CableBox-BF58','ymn5gzm5um')
client = mqttSetup()
client.publish(b'/response', b'Goodmorning!')

timer = 60
period = 0.5

while True:
    try:
        client.check_msg()
        timer -= period
        sleep(period)
        if timer % 5 == 0:
            print ("Time to sleep:", timer)
        if timer <= 0:
            break


    except OSError as e:
        restart_and_reconnect()


goToSleep(minutes=15)


