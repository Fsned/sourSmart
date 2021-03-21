# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()
# Complete project details at https://RandomNerdTutorials.com
  
from time import sleep
import network

def connectWifi(ssid='CableBox-BF58', psk='ymn5gzm5um'):
    
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(ssid, psk)
    
    for a in range(10):
        if station.isconnected():
            print('Connection successful')
            print(station.ifconfig())
            return True
        
        sleep(1)

    return False

connectWifi()
