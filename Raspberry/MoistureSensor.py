import RPi.GPIO as GPIO
import time as time
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN)

class MoistureSensor():
    def __init__(self):
        self.pin=21
    
    def getValue(self):
        #0 stand for very very high moisture, 1 stands for not that very high moisutre
        return GPIO.input(21)