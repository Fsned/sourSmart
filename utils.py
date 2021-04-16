import network          # Used for the connectWifi method

from time import sleep

def connectWifi(ssid='CableBox-BF58', psk='ymn5gzm5um'):
    
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(ssid, psk)
    
    for a in range(10):
        if station.isconnected():
            ip = station.ifconfig()
            print("Wifi connected successfully", ip[0])
            #
            #print
            #print('Connection successful')
#
            #
            #print(station.ifconfig())
            return True
        
        sleep(1)

    return False




def blinkSequence(ledObject, blinks=1, onTime = 0.2, offTime = 0.25):
    if ledObject.value():
        ledObject.value(0)
        sleep(0.2)

    for a in range(blinks):
        ledObject.value(1)
        sleep(onTime)
        ledObject.value(0)
        sleep(offTime)







