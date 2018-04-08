#from Adafruit_PWM_Servo_Driver import PWM
import time



class RobotArm(object):

    activeServos=[]
    ServosMin=[]
    ServosMax=[]
    ServosPos=[]
    
    def __init__(self):        
        #pwm=PWM(0x40)                       # Initialise the PWM device using the default address
        #pwm.setPWMFreq(60)                  # Set frequency to 60 Hz
        RobotArm.activeServos.append(0)
        for i in range(1,6):
            RobotArm.activeServos.append(1)
        for i in range(0,6):
            RobotArm.ServosMin.append(60)
            RobotArm.ServosMax.append(120)
            RobotArm.ServosPos.append(90)
            RobotArm.moveServo(self,i,90)
            
        
        

    def setServoPulse1(channel, pulse):
        pulseLength = 1000000                   # 1,000,000 us per second
        pulseLength /= 60                       # 60 Hz
        print ("%d us per period") % pulseLength
        pulseLength /= 4096                     # 12 bits of resolution
        print ("%d us per bit") % pulseLength
        pulse *= 1000
        pulse /= pulseLength
        #pwm.setPWM(channel, 0, pulse)

        
    def setServoPulse(channel,pulse):
        print(channel,pulse)
        
    def moveServo(self,channel,degrees):
        if(RobotArm.activeServos[channel]==1):
            if degrees<RobotArm.ServosMin[channel]: degrees=RobotArm.ServosMin[channel]
            if degrees>RobotArm.ServosMax[channel]: degrees=RobotArm.ServosMax[channel]
            
            print (min(RobotArm.ServosPos[channel],degrees))
            print (max(RobotArm.ServosPos[channel],degrees))
            
            for i in range(min(RobotArm.ServosPos[channel],degrees),max(RobotArm.ServosPos[channel],degrees)):
                RobotArm.setServoPulse(channel,4096/180*degrees*RobotArm.activeServos[channel])
                time.sleep(0.05)
            
        
rb=RobotArm()
rb.moveServo(2,110)
