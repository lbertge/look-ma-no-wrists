import sys
sys.path.insert(0, 'imagezmq/imagezmq')
import imagezmq

import socket
import time
import cv2
import imagezmq
import numpy as np
import webcam

class ImageSender:
    def __init__(self, connect_to):
        self.sender = imagezmq.ImageSender(connect_to=connect_to)
        self.name = socket.gethostname()
    
    def send_image(self, image):
        reply =  self.sender.send_image(self.name, image)
        if reply != b'':
            out = np.fromstring(reply, np.float32)
            out = out.reshape((-1, 4))
            out = np.atleast_2d(out).tolist()
        else:
            out = None
        return out 

if __name__ == '__main__':
    print("Test send images to socket")
    image1 = np.zeros((400, 400, 3), dtype='uint8')
    green = (0, 255, 0)
    sender = ImageSender(connect_to='tcp://192.168.1.86:5555')

    while True:
        reply = sender.send_image(image1)
        array = np.fromstring(reply)
        print(array)

        time.sleep(1)

