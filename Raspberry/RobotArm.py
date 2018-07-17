from Adafruit_PWM_Servo_Driver import PWM
import time





class RobotArm(object):
    
    #the speed at which servos for a change of 1 in the pwm pulse signal
    servoSpeed=0.02
    
    #minimal and maximal pulse length for pwm for the big servos
    minPulse=1721
    maxPulse=1980
    #S stands for the smaller type servos
    minPulseS=0
    maxPulseS=0
    
    #array containing information about which servos we can use
    activeServos=[]
    
    #arrays containing information that is used to limit the servos movements
    servosMin=[]
    servosMax=[]
    
    #array containing information about the current position of the servos
    servosPos=[]
    
    pwm=PWM(0x40)                       # Initialise the PWM device using the default address
    pwm.setPWMFreq(60)                  # Set frequency to 60 Hz
    
    def __init__(self):
        
        numServo=7
        #filling the arrays with default information
        RobotArm.activeServos.append(0)
        RobotArm.activeServos.append(0)
        for i in range(2,numServo):
            RobotArm.activeServos.append(1)
        for i in range(0,numServo):
            RobotArm.servosMin.append(30)
            RobotArm.servosMax.append(150)
            RobotArm.servosPos.append(90)
            
        #setting a minimum and maximum degrees for specific servos
        RobotArm.servosMin[1]=140
        RobotArm.servosMax[1]=180
        RobotArm.servosMax[3]=180
        RobotArm.servosPos[1]=141
        RobotArm.servosMin[2]=60
        RobotArm.servosMax[2]=180
        
        self.turnOffAll()
        
        #not used
    def setServoPulseHigher(channel, pulse):
        #setting up the pwm frequency and pulse length
        pulseLength = 1000000                   # 1,000,000 us per second
        pulseLength /= 60                       # 60 Hz
        print ("%d us per period" % pulseLength)
        pulseLength /= 4096                     # 12 bits of resolution
        print ("%d us per bit" % pulseLength)
        pulse *= 1000
        pulse /= pulseLength
        RobotArm.pwm.setPWM(channel, 0, int(pulse))
        
        #not used
    def setServoPulseLower(channel, pulse):
        pulseLength = 1000000                   # 1,000,000 us per second
        pulseLength /= 60                       # 60 Hz
        print ("%d us per period" % pulseLength)
        pulseLength /= 4096                     # 12 bits of resolution
        print ("%d us per bit" % pulseLength)
        pulse *= 1000
        pulse /= pulseLength
        RobotArm.pwm.setPWM(channel, int(pulse),0)


        
    def setServoPulse1(channel,pulse):
        print(channel,pulse)
        
    def moveServo(self,channel,degrees):
        
        #print (RobotArm.activeServos[channel])
        
        if(RobotArm.activeServos[channel]==1):
            if degrees<RobotArm.servosMin[channel]: degrees=RobotArm.servosMin[channel]
            if degrees>RobotArm.servosMax[channel]: degrees=RobotArm.servosMax[channel]
            
            #print (min(RobotArm.servosPos[channel],degrees))
            #print (max(RobotArm.servosPos[channel],degrees))
            
            #determines if the loop for changing servos goes forward or backwards
            step=1
            if RobotArm.servosPos[channel]>degrees: step=-1
            
            
            minPulse=RobotArm.minPulse
            degree=(RobotArm.maxPulse-RobotArm.minPulse)/180  #calculating the pulse needed for a change in 1 degree
            
            start=int(minPulse+degree*RobotArm.servosPos[channel])
            end=int(minPulse+degree*degrees)
            
            #loop for slowly changing the servo position
            for i in range(start,end,step):
                #print (i)
                #RobotArm.setServoPulse(channel,int((4096/180)*degrees))
                #RobotArm.setServoPulseHigher(channel,int((4096/180)*i))       
                #RobotArm.setServoPulseHigher(channel, i)
                RobotArm.pwm.setPWM(channel,i,4096-i)
                time.sleep(RobotArm.servoSpeed)
             
            RobotArm.servosPos[channel]=degrees
    
    def turnOff(self,channel):
        RobotArm.pwm.setPWM(channel,0,0)
    
    def turnOffAll(self):
        for x in range(0,6):
            RobotArm.turnOff(self,x)
            
    def cameraPosition(self):
        #self.moveServo(1,150)
        #time.sleep(0.5)
        self.turnOffAll()
        self.moveServo(2,150)
        time.sleep(0.5)
        self.moveServo(3,180)
        time.sleep(0.5)
        self.moveServo(4,120)
        time.sleep(0.5)
        self.moveServo(6,60)
        time.sleep(0.5)
        
    def insertSensorPosition(self):
        self.turnOffAll()
        self.moveServo(3,120)
        self.moveServo(2,180)
        self.moveServo(3,120)
        
    def insertSensorPosition1(self):
        self.moveServo(2,170)
        self.moveServo(3,110)
        
    def insertSensor(self):
        self.moveServo(2,140)
        

    #def standUp(self):
    #   self.moveServo(1,150)
    #    self.moveServo(2,180)
     #   self.moveServo(3,90)
    
