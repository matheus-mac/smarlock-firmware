import RPi.GPIO as gpio
import time

gpio.setmode(gpio.BOARD)
def portaoAberto():
    PIN = 29
    gpio.setup(PIN, gpio.IN, pull_up_down = gpio.PUD_DOWN)
    if (gpio.input(PIN)==0):
        return False
    else:
        return True