import RPi.GPIO as GPIO
import time, datetime
from time import sleep

GPIO.setmode(GPIO.BCM)

#Droid
interval = 0.1
PWMA = 5
AIN1 = 13
AIN2 = 6
PWMB = 23
BIN1 = 24
BIN2 = 25
STBY = 19

rotor = { 'PWMA', 'AIN1', 'AIN2', 'PWMB', 'BIN1', 'BIN2', 'STBY' }


GPIO.setup(AIN1, GPIO.OUT)
GPIO.setup(AIN2, GPIO.OUT)
GPIO.setup(PWMA, GPIO.OUT)
GPIO.setup(BIN1, GPIO.OUT)
GPIO.setup(BIN2, GPIO.OUT)
GPIO.setup(PWMB, GPIO.OUT)
GPIO.setup(STBY, GPIO.OUT)



class Pidro(object):

    def r(self):
        (GPIO.output(AIN1, GPIO.HIGH))
        (GPIO.output(AIN2, GPIO.LOW))
        (GPIO.output(PWMA, GPIO.HIGH))
        (GPIO.output(BIN1, GPIO.HIGH))
        (GPIO.output(BIN2, GPIO.LOW))
        (GPIO.output(PWMB, GPIO.HIGH))
        (GPIO.output(STBY, GPIO.HIGH))

    def l(self):
        (GPIO.output(AIN1, GPIO.LOW))
        (GPIO.output(AIN2, GPIO.HIGH))
        (GPIO.output(PWMA, GPIO.HIGH))
        (GPIO.output(BIN1, GPIO.LOW))
        (GPIO.output(BIN2, GPIO.HIGH))
        (GPIO.output(PWMB, GPIO.HIGH))
        (GPIO.output(STBY, GPIO.HIGH))

    def b(self):
        (GPIO.output(AIN1, GPIO.HIGH))
        (GPIO.output(AIN2, GPIO.LOW))
        (GPIO.output(PWMA, GPIO.HIGH))
        (GPIO.output(BIN1, GPIO.LOW))
        (GPIO.output(BIN2, GPIO.HIGH))
        (GPIO.output(PWMB, GPIO.HIGH))
        (GPIO.output(STBY, GPIO.HIGH))


    def f(self):
        (GPIO.output(AIN1, GPIO.LOW))
        (GPIO.output(AIN2, GPIO.HIGH))
        (GPIO.output(PWMA, GPIO.HIGH))
        (GPIO.output(BIN1, GPIO.HIGH))
        (GPIO.output(BIN2, GPIO.LOW))
        (GPIO.output(PWMB, GPIO.HIGH))
        (GPIO.output(STBY, GPIO.HIGH))


    def s(self):
        (GPIO.output(AIN1, GPIO.LOW))
        (GPIO.output(AIN2, GPIO.LOW))
        (GPIO.output(PWMA, GPIO.LOW))
        (GPIO.output(BIN1, GPIO.LOW))
        (GPIO.output(BIN2, GPIO.LOW))
        (GPIO.output(PWMB, GPIO.LOW))
        (GPIO.output(STBY, GPIO.LOW))
