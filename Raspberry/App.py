import socket
from threading import *
import motorTest as Motors
import RobotArm as Arm
import io
import socket
import struct
import time
import picamera


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
        
        
class sendStream(Thread):

    def __init__(self,pcname):
        Thread.__init__(self)
        self.client_socket = socket.socket()
        self.client_socket.connect((pcname, 8000))#pc
        self.connection = self.client_socket.makefile('wb')
        self.start()
    
    def run(self):
        try:
           output = SplitFrames(self.connection)
           with picamera.PiCamera(resolution='1280x720', framerate=24) as camera:
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
sendStream('192.168.0.103')
while 1:
    clientSocket, address = serversocket.accept()
    client(clientSocket, address)

