import io
import socket
import struct
import cv2
import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile
import time
import GUI as GUI
import threading
from collections import defaultdict
from io import StringIO
from PIL import Image
import ctypes
import queue

#sys.path.insert(0, 'C:\\Users\\Boris\\Downloads\\models-master\\models-master\\research\\object_detection')


raspberrypiIp=""

try:
  f=open("options.txt","r")
  raspberrypiIp=f.readline()
  f.close
except:
  ctypes.windll.user32.MessageBoxW(None, u"There was an error in loading options", u"Error", 0)


if tf.__version__ < '1.4.0':
  raise ImportError('Please upgrade your tensorflow installation to v1.4.* or later!')


#The queue where we will store the data that will be send to the robot
dataQueue=queue.Queue()

#A thread class used for sending the data from the UI and Computer Vision
        
#Method for putting data to the queue
def addDataToQueue(string):
  dataQueue.put(string)


#Creating a thread for the UI
class UIThread(threading.Thread):
  def __init__(self,i,timer):
    threading.Thread.__init__(self)
    self.i=i
    self.timer=timer
  def run(self):
    self.UI=GUI.RobotPlantCare(addDataToQueue)
    self.UI.mainloop()


    
#Running the threads
thread=UIThread(1,1)
thread.start()

#sys.path.append('C:\\Users\\Boris\\Downloads\\models-master\\models-master\\research') # point to your tensorflow dir
#sys.path.append('C:/Users/Boris/Downloads/models-master/models-master/research/slim') # point ot your slim dir


print("Working till now")

from utils import label_map_util
from utils import visualization_utils as vis_util


# What model to use.
MODEL_NAME = 'pot_graph'

# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = os.path.join('training', 'object-detection.pbtxt')

NUM_CLASSES = 1

#Load a (frozen) Tensorflow model into memory
detection_graph = tf.Graph()
with detection_graph.as_default():
  od_graph_def = tf.GraphDef()
  with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
    serialized_graph = fid.read()
    od_graph_def.ParseFromString(serialized_graph)
    tf.import_graph_def(od_graph_def, name='')

#Load a label map
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)


#Storing an image as a numpy array
def load_image_into_numpy_array(image):
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape(
      (im_height, im_width, 3)).astype(np.uint8)

print("Starting Socket Connections")

#Client socket used to send data back to the raspberry
isconnected=0
while isconnected==0:
  try:
    client_socket=socket.socket()
    client_socket.connect((raspberrypiIp,8003))#raspberry
    ctypes.windll.user32.MessageBoxW(None, u"Successful connection to robot", u"It worked!", 0)
    isconnected=1
  except:
    ctypes.windll.user32.MessageBoxW(None, u"There was an error in connection to robot. Trying again!", u"Error", 0)


#Now that we have where to send data we can auctally start sending the data
class sendDataThread(threading.Thread):
  def __init__(self,i,timer):
    threading.Thread.__init__(self)
    self.i=i
    self.timer=timer

  def run(self):
    while True:
      time.sleep(0.0001)
      while not dataQueue.empty():
        try:
          data=dataQueue.get()
          if data!='':
            client_socket.send((data+";").encode())
            time.sleep(0.0001)
        except:
          ctypes.windll.user32.MessageBoxW(None, u"There was an error in connection", u"Error", 0)


thread=sendDataThread(1,1)
thread.start()


#Server socket used to recieve the data from the raspberry    
server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8000))
server_socket.listen(0)
#Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('rwb')


try:
    with detection_graph.as_default():
      with tf.Session(graph=detection_graph) as sess:
        # Definite input and output Tensors for detection_graph
        image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
        # Each box represents a part of the image where a particular object was detected.
        detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
        # Each score represent how level of confidence for each of the objects.
        # Score is shown on the result image, together with the class label.
        detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
        detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
        num_detections = detection_graph.get_tensor_by_name('num_detections:0')
        while True:


            # Read the length of the image as a 32-bit unsigned int. If the
            # length is zero, quit the loop
            
            
            image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
            if not image_len:
                break
            # Construct a stream to hold the image data and read the image
            # data from the connection
            image_stream = io.BytesIO()
            image_stream.write(connection.read(image_len))
 
            # Rewind the stream, open it as an image with PIL and do some   
            # processing on it
            image_stream.seek(0)
            image_np = Image.open(image_stream).rotate(90)
            b, g, r = image_np.split()
            image_np = Image.merge("RGB", (r, g, b))
            image_np=np.array(image_np)
            image_np_expanded = np.expand_dims(image_np, axis=0)

            # Actual detection.
            (boxes, scores, classes, num) = sess.run(
            [detection_boxes, detection_scores, detection_classes, num_detections],
            feed_dict={image_tensor: image_np_expanded})
            
            #Visualization of the results of a detection.
            squeezed_scores=np.squeeze(scores)
            squeezed_boxes=np.squeeze(boxes)
            vis_util.visualize_boxes_and_labels_on_image_array(
            image_np,
            squeezed_boxes,
            np.squeeze(classes).astype(np.int32),
            squeezed_scores,
            category_index,
            use_normalized_coordinates=True,
            line_thickness=8)


            #saving the results from the object detection
            max_boxes_to_draw=20
            if not max_boxes_to_draw:
              max_boxes_to_draw = squeezed_boxes.shape[0]
            min_score_thresh=.5

            detections_coordinates="Detection: "

            scoreslen=len(squeezed_scores)
            #print("len",scoreslen)

            coordinates=""
            for i in range(min(max_boxes_to_draw, squeezed_boxes.shape[0])):
               if squeezed_scores is None or squeezed_scores[i] > min_score_thresh:
                 a=str(squeezed_boxes[i][0])[0:5]
                 b=str(squeezed_boxes[i][1])[0:5]
                 c=str(squeezed_boxes[i][2])[0:5]
                 d=str(squeezed_boxes[i][3])[0:5]
                 x=str(squeezed_scores[i])[0:4]
                 coordinates+=str(i)+" "+x+" "+a+" "+b+" "+c+" "+d+" "
                 #print (str(i)," ", str(squeezed_boxes[i][0])," ", str(squeezed_boxes[i][1]), " ",str(squeezed_boxes[i][2])," ", str(squeezed_boxes[i][3]))

            detections_coordinates+=coordinates
            print(detections_coordinates)
            addDataToQueue(detections_coordinates)
            
            #Visualising the camera stream
            cv2.imshow('Stream',image_np) 
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

finally:
    connection.close()
    server_socket.close()
