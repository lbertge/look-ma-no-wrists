import cv2
from threading import Thread

class WebcamVideoStream:
    def __init__(self, src, width, height):
        self.stream = cv2.VideoCapture(src)
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        print(width, height)
        print(self.stream.get(cv2.CAP_PROP_FRAME_HEIGHT), self.stream.get(cv2.CAP_PROP_FRAME_WIDTH))
        (self.grabbed, self.frame) = self.stream.read()

        self.stopped = False

    def start(self):
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        while True:
            if self.stopped:
                return

            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        return self.frame

    def size(self):
        return self.stream.get(3), self.stream.get(4)

    def stop(self):
        self.stopped = True
