import RPi.GPIO as GPIO
import time, datetime
from time import sleep

GPIO.setmode(GPIO.BCM)

#Droid
interval = 0.1
PWMA = 22
AIN1 = 18
AIN2 = 27
STBY = 17

rotor = { 'PWMA', 'AIN1', 'AIN2', 'PWMB', 'BIN1', 'BIN2', 'STBY' }


GPIO.setup(AIN1, GPIO.OUT)
GPIO.setup(AIN2, GPIO.OUT)
GPIO.setup(PWMA, GPIO.OUT)
GPIO.setup(STBY, GPIO.OUT)
#GPIO.cleanup()


class Pump(object):

    #method for turning the servo on
    def on(self,dur):
        (GPIO.output(AIN1, GPIO.LOW))
        (GPIO.output(AIN2, GPIO.HIGH))
        (GPIO.output(PWMA, GPIO.HIGH))
        (GPIO.output(STBY, GPIO.HIGH))
        time.sleep(dur)
        self.off()
        

    #method for turning the servo off
    def off(self):
        (GPIO.output(AIN1, GPIO.LOW))
        (GPIO.output(AIN2, GPIO.LOW))
        (GPIO.output(PWMA, GPIO.LOW))
        (GPIO.output(STBY, GPIO.LOW))

