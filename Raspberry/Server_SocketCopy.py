import socket
from threading import *
import motorTest as Motors
import RobotArm as Arm

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = ""#raspberry
port = 8003
print (host)
print (port)
serversocket.bind((host, port))
rb=Arm.RobotArm()
car=Motors.Car()


rb=Arm.RobotArm()
rb.moveServo(1,140)
rb.moveServo(2,30)
rb.moveServo(3,180)
car=Motors.Car()


class client(Thread):
    def __init__(self, socket, address):
        Thread.__init__(self)
        self.sock = socket
        self.addr = address
        self.start()

    def run(self):
        while 1:
            data=self.sock.recv(1024).decode()
            print('Client sent:', data)
            coordinates=data.split()
            print (len(data))
            
            
            

serversocket.listen(5)
print ('server started and listening')

while 1:
    clientsocket, address = serversocket.accept()
    client(clientsocket, address)

