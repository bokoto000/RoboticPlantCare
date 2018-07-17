import RPi.GPIO as GPIO
import time, datetime
from time import sleep

GPIO.setmode(GPIO.BCM)

#Defining pins
interval = 0.1
PWMA = 5
AIN1 = 6
AIN2 = 13
PWMB = 23
BIN1 = 24
BIN2 = 25
STBY = 19

rotor = { 'PWMA', 'AIN1', 'AIN2', 'PWMB', 'BIN1', 'BIN2', 'STBY' }

#setting up pins
GPIO.setup(AIN1, GPIO.OUT)
GPIO.setup(AIN2, GPIO.OUT)
GPIO.setup(PWMA, GPIO.OUT)
GPIO.setup(BIN1, GPIO.OUT)
GPIO.setup(BIN2, GPIO.OUT)
GPIO.setup(PWMB, GPIO.OUT)
GPIO.setup(STBY, GPIO.OUT)
#GPIO.cleanup()


class Car(object):
    
    
    #all the methods below are used to control the motor so that the car moves according to the name
    #S stands for Stops after a duration
    def leftS(self,duration):
        (GPIO.output(AIN1, GPIO.HIGH))
        (GPIO.output(AIN2, GPIO.LOW))
        (GPIO.output(PWMA, GPIO.HIGH))
        (GPIO.output(BIN1, GPIO.HIGH))
        (GPIO.output(BIN2, GPIO.LOW))
        (GPIO.output(PWMB, GPIO.HIGH))
        (GPIO.output(STBY, GPIO.HIGH))
        time.sleep(duration)
        self.stop()
        
    def left(self):
        (GPIO.output(AIN1, GPIO.HIGH))
        (GPIO.output(AIN2, GPIO.LOW))
        (GPIO.output(PWMA, GPIO.HIGH))
        (GPIO.output(BIN1, GPIO.HIGH))
        (GPIO.output(BIN2, GPIO.LOW))
        (GPIO.output(PWMB, GPIO.HIGH))
        (GPIO.output(STBY, GPIO.HIGH))
        

    def rightS(self,duration):
        (GPIO.output(AIN1, GPIO.LOW))
        (GPIO.output(AIN2, GPIO.HIGH))
        (GPIO.output(PWMA, GPIO.HIGH))
        (GPIO.output(BIN1, GPIO.LOW))
        (GPIO.output(BIN2, GPIO.HIGH))
        (GPIO.output(PWMB, GPIO.HIGH))
        (GPIO.output(STBY, GPIO.HIGH))
        time.sleep(duration)
        self.stop()
    
    def right(self):
        (GPIO.output(AIN1, GPIO.LOW))
        (GPIO.output(AIN2, GPIO.HIGH))
        (GPIO.output(PWMA, GPIO.HIGH))
        (GPIO.output(BIN1, GPIO.LOW))
        (GPIO.output(BIN2, GPIO.HIGH))
        (GPIO.output(PWMB, GPIO.HIGH))
        (GPIO.output(STBY, GPIO.HIGH))
        

    def backS(self,duration):
        (GPIO.output(AIN1, GPIO.HIGH))
        (GPIO.output(AIN2, GPIO.LOW))
        (GPIO.output(PWMA, GPIO.HIGH))
        (GPIO.output(BIN1, GPIO.LOW))
        (GPIO.output(BIN2, GPIO.HIGH))
        (GPIO.output(PWMB, GPIO.HIGH))
        (GPIO.output(STBY, GPIO.HIGH))
        time.sleep(duration)
        self.stop()
        
    def back(self):
        (GPIO.output(AIN1, GPIO.HIGH))
        (GPIO.output(AIN2, GPIO.LOW))
        (GPIO.output(PWMA, GPIO.HIGH))
        (GPIO.output(BIN1, GPIO.LOW))
        (GPIO.output(BIN2, GPIO.HIGH))
        (GPIO.output(PWMB, GPIO.HIGH))
        (GPIO.output(STBY, GPIO.HIGH))


    def forwardS(self,duration):
        (GPIO.output(AIN1, GPIO.LOW))
        (GPIO.output(AIN2, GPIO.HIGH))
        (GPIO.output(PWMA, GPIO.HIGH))
        (GPIO.output(BIN1, GPIO.HIGH))
        (GPIO.output(BIN2, GPIO.LOW))
        (GPIO.output(PWMB, GPIO.HIGH))
        (GPIO.output(STBY, GPIO.HIGH))
        time.sleep(duration)
        self.stop()
        
    def forward(self):
        (GPIO.output(AIN1, GPIO.LOW))
        (GPIO.output(AIN2, GPIO.HIGH))
        (GPIO.output(PWMA, GPIO.HIGH))
        (GPIO.output(BIN1, GPIO.HIGH))
        (GPIO.output(BIN2, GPIO.LOW))
        (GPIO.output(PWMB, GPIO.HIGH))
        (GPIO.output(STBY, GPIO.HIGH))

    def stop(self):
        (GPIO.output(AIN1, GPIO.LOW))
        (GPIO.output(AIN2, GPIO.LOW))
        (GPIO.output(PWMA, GPIO.LOW))
        (GPIO.output(BIN1, GPIO.LOW))
        (GPIO.output(BIN2, GPIO.LOW))
        (GPIO.output(PWMB, GPIO.LOW))
        (GPIO.output(STBY, GPIO.LOW))
        
        
