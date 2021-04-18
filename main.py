
from machine import Pin, I2C, reset, unique_id, deepsleep
from ubinascii import hexlify
from random import randint
from utime import sleep
import ujson
import utils
import simple                       # Used by MQTT
import esp32
import sensors


def publishGraph(interval=1):
    temp = {}

    with open ('data.json', 'r') as dataFile:
        temp = ujson.load(dataFile)

    data = {}
    temperature = []
    humidity = []
    height = []

    samplesTaken = 0
    i = 0

    for a in range(0, len(temp['temperature'])):
        try:
            if i % interval == 0:
                temperature.append(temp['temperature'][i])
                humidity.append(temp['humidity'][i])
                height.append(temp['height'][i])
                samplesTaken += 1
            i += 1
        except:
            print ("exception!!")

    for a in range(20 - len(temp['temperature'])):
        temperature.insert(0, 0)
        humidity.insert(0,0)
        height.insert(0,0)

    data['temperature'] = temperature
    data['humidity'] = humidity
    data['height'] = height

    client.publish(b'/sourSmart/out/graphData', str(data).encode(), retain=True)
    print ("Published graphdata:", data)




def callbackFunction(topic, msg):
    global client

    msg = msg.decode('utf-8')
    topic = topic.decode('utf-8')

    print ("Received:", msg, "on topic:", topic)
    ### If we received a command, handle it here:
    if topic == '/sourSmart/in/command':
        if msg == 'ping':
            client.publish(b'/sourSmart/out/response', b'pong')
        
        elif msg == 'restart':
            client.publish(b'/sourSmart/out/response', b'restarting in 5...')
            sleep(5)
            reset()

        elif msg == 'timer':
            client.publish(b'/sourSmart/out/response',b'Time to sleep: ' + str(timer))

    ### If we received a setGraphInterval request, handle it here
    elif topic == '/sourSmart/in/setGraphInterval':
        
        publishGraph(interval=int(msg))

    elif topic == '/sourSmart/in/toggleFeed':
        temp = {}

        with open ('data.json', 'r') as dataFile:
            temp = ujson.load(dataFile)

        response = {}
        response['time'] = msg
        response['currentHeight'] = temp['height'][-1]

        client.publish(b'/sourSmart/out/feedData', str(response).encode())
        
    else:
        print ("Received unhandled topic message", topic, msg)



def buttonJob(buttonInput):
    global timer

    if  not buttonInput.value():    # Button goes low on click, so if buttonInput == 0, means 'if button is clicked', prevents debouncing outputs on release
        timer += 60 # add seconds to the timer...
        print ("New timer:", timer)



def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  sleep(10)
  reset()


def mqttSetup():
    mqtt_server = '135.181.193.6'
    client_id = hexlify(unique_id())
    topic = '/sourSmart/in/#'
    client = simple.MQTTClient(client_id, mqtt_server)
    client.set_callback(callbackFunction)
    client.connect()

    try:
        client.subscribe(topic.encode('utf-8'))
        print ("Subscribed to", topic)
    except:
        print ("Couldn't subscribe to", topic)
        restart_and_reconnect()

    print('Connected to %s MQTT broker' % (mqtt_server))
    return client


def goToSleep(minutes=1):
    sleepString = 'Sleeping for' + str(minutes) + 'minutes'
    client.publish(b'/sourSmart/out/response',sleepString.encode('utf-8'))

    sleep(2)

    deepsleep(minutes * 60 * 1000)


##### Bootup
### Button setup
buttonInput = Pin(35, Pin.IN)
buttonInput.irq(trigger=Pin.IRQ_FALLING, handler=buttonJob)
esp32.wake_on_ext0(pin = buttonInput, level = esp32.WAKEUP_ALL_LOW)

### Wifi connect
utils.connectWifi('CableBox-BF58','ymn5gzm5um')

### MQTT Client setup
client = mqttSetup()

### Collect a data point and publish it
sensors.sensorCollectionJob()

### Publish current graphs
publishGraph(1)

### Set a timer to stay alive for 60 seconds
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
            goToSleep(minutes=15)

    except OSError as e:
        restart_and_reconnect()
