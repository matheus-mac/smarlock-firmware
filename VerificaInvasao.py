import RPi.GPIO as gpio
import time
 
def verificaArrombamento():
    PIN = 31
    gpio.setup(PIN, gpio.IN, pull_up_down = gpio.PUD_DOWN)
    if (gpio.input(PIN)==1):
        return False
    else:
        return True
