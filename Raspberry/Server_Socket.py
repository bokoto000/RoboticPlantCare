import socket
from threading import *
import Car as Motors
import RobotArm as Arm
import Pump as Pump
import MoistureSensor as MoistureSensor
import io
import socket
import struct


import time
import picamera
import decimal

dec=decimal.Decimal

pcIp=""
f=open("options.txt","r")
pcIp=f.readline()

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = ""#raspberry
port = 8003
print (host)
print (port)
serversocket.bind((host, port))

ra=Arm.RobotArm()
car=Motors.Car()
pump=Pump.Pump()
msensor=MoistureSensor.MoistureSensor()


wateringAmount50ml=3.4
minx=0.45
maxx=0.6
steeringTime=0.2
fixedTravel=True
fixedDist=1
afterSuccessRotation=1

ra=Arm.RobotArm()
ra.cameraPosition()
car=Motors.Car()
car.stop()


timing=0
options=[]

#get raspberry frames and stream them to pc
class SplitFrames(object):
    def __init__(self, connection):
       self.connection = connection
       self.stream = io.BytesIO()
       self.count = 0

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # Start of new frame; send the old one's length
            # then the data
            size = self.stream.tell()
            if size > 0:
                self.connection.write(struct.pack('<L', size))
                self.connection.flush()
                self.stream.seek(0)
                self.connection.write(self.stream.read(size))
                self.count += 1
                self.stream.seek(0)
        self.stream.write(buf)
        
#The thread that sends the stream        
class sendStream(Thread):

    def __init__(self,pcname):
        Thread.__init__(self)
        self.client_socket = socket.socket()
        tryconnection = 0
        while tryconnection is 0:
            try:
                self.client_socket.connect((pcname, 8000))#pc
                self.connection = self.client_socket.makefile('wb')
                tryconnection=1
            except:
                pass
        self.start()
    
    def run(self):
        try:
           output = SplitFrames(self.connection)
           with picamera.PiCamera(resolution='720x720', framerate=24) as camera:
                time.sleep(2)
                print("starts sending")
                start = time.time()
                camera.start_recording(output, format='mjpeg')
                camera.wait_recording(10000000)
                camera.stop_recording()
                # Write the terminating 0-length to the connection to let the
                # server know we're doneq
                self.connection.write(struct.pack('<L', 0))
        finally:
            self.connection.close()
            self.client_socket.close()
            finish = timqe.time()
            print('Sent %d images in %d seconds at %.2ffps' % (
            output.count, finish-start, output.count / (finish-start)))
        
#the thread that gets data from pc
class client(Thread):
    def __init__(self, socket, address):
        Thread.__init__(self)
        self.sock = socket
        self.addr = address
        self.start()
        
    #the user wants to start the plant care while he is on a vacation. Realised by this method. Called when clicked the send options button    
    def getOptions(self,data):
        
        #setting user's options
        options=data
        timing=data[1]
        print (options)
        numSettings=len(options)-3
        potsFound=0
        
        #making a full circle checking for plants
        for i in range(0,50):
            
            successfulchecks=0
            successfulsize=0
            
            #waiting for the data to stabilize.
            for j in range(0,80):
                splitDatas=self.sock.recv(1024).decode().split(';')
                
            #checking 10 times if there is plant or not
            for j in range(0,10):
                
                splitDatas=self.sock.recv(1024).decode().split(';')
                
                for splitDataString in splitDatas:
                    
                    splitData=splitDataString.split(' ')
                    
                    
                    if splitData[0] is "Direct":
                            if splitData[1] is "S":
                                return
                            
                            
                    if splitData[0]=='Detection:':
                        if len(splitData)>5 :
                            for no in range(0,int(len(splitData)/6)):
                                percentsure=dec(splitData[2])
                                a=dec(splitData[3])
                                b=dec(splitData[4])
                                c=dec(splitData[5])
                                d=dec(splitData[6])
                                xpos=(d+b)/2
                                checksize=(c-a)*(d-b)

                                if xpos>minx and xpos<maxx:
                                    successfulsize+=checksize
                                    successfulchecks+=1
                                    
             #do the caring part for the plant (getting close, using all the sensors,wateringand going back                      
            if successfulchecks>=8 :
                
                
                print("Succ")
                successfulsize=dec(successfulsize/successfulchecks)
                print (successfulsize)
                k=dec(0.23)
                print(dec(1/successfulsize)*k)
                car.forwardS(dec(1/successfulsize)*k)
                if fixedTravel is True:
                    car.forwardS(fixedDist)
                else:
                    car.forwardS(dec(1/successfulsize)*k)
                time.sleep(2)
                ra.insertSensorPosition()
                time.sleep(1)
                ra.insertSensor()
                time.sleep(1)
                #check if the moisture is really too high
                if msensor.getValue()==1:
                    if potsFound<numSettings:
                        print ((1/(50/int(options[potsFound+2])))*wateringAmount50ml)
                        pump.on((1/(50/int(options[numSettings])))*wateringAmount50ml)
                    else:
                        pump.on(wateringAmount50ml)
                        print(wateringAmount50ml)
                time.sleep(1)
                ra.insertSensorPosition()
                time.sleep(1)
                car.backS((1/successfulsize)*k)
                time.sleep(1)
                ra.cameraPosition()
                potsFound+=1
                car.rightS(afterSuccessRotation)
                
            
            car.rightS(steeringTime)
        
                    
                
                    
            
                
    #applying the user manual control
    def getDirection(self,splitData):
        direction=splitData[1]
        print (direction)
        if direction is 'F':
            car.forward()
        if direction is 'B':
            car.back()
        if direction is 'R':
            car.right()
        if direction is 'L':
            car.left()
        if direction is 'S':
            car.stop()
            
    
        
    #running the thread for getting all the user input
    def run(self):
        while 1:
            datas=self.sock.recv(1024).decode().split(";")
            for data in datas:
                #print('Client sent:', data)
                splitData=data.split(' ')
                if splitData[0]=="Options":
                    self.getOptions(splitData)
                    
                if splitData[0]=="Direct":
                    self.getDirection(splitData)
                if splitData[0]=="Detection:" and len(splitData)>6:
                    x=dec(splitData[2])
                    a=dec(splitData[3])
                    b=dec(splitData[4])
                    c=dec(splitData[5])
                    d=dec(splitData[6])
                    #print((c+a)/2," ",(d+b)/2)
            
            

serversocket.listen(5)
print ('server started and listening')
#a thread to search and connect to pc even after he disconnects
class searchForServer(Thread):
    
    def __init__(self):
        Thread.__init__(self)
        self.start()
        
    def run(self):
        while 1:
            clientSocket, address = serversocket.accept()
            client(clientSocket, address)

searchForServer()
sendStream(pcIp)
