from commands import command_dict
from bounds import in_bounds
import numpy as np
from collections import deque
import logging
import time

class CommandManager:
    def __init__(self, delay=1, qsize=10):
        self.delay = delay
        self.last_act = 0

        # remember the last qsize frames
        self.queue = deque(maxlen=qsize)
        self.qsize = qsize

        logging.basicConfig(level=logging.INFO)

    def recv_boxes(self, boxes):
        if len(boxes) == 1:
            mdpt = self.process_single_hand(boxes[0])
        else:
            mdpts = self.process_dual_hand(boxes)

    def process_single_hand(self, box):
        mdpt = self.midpoint(box)

        command = self.in_bounds(mdpt)
        if command:
            self.action(command)

    def action(self, command):
        if time.time() - self.last_act > self.delay:
            if command in command_dict:
                command_dict[command].f()
            self.last_act = time.time()

    def in_bounds(self, midpoint):
        return in_bounds(midpoint, command_dict)

    def process_dual_hand(self, boxes):
        # euclid distance
        mdpt1 = self.midpoint(boxes[0])
        mdpt2 = self.midpoint(boxes[1])
        dist = np.linalg.norm(mdpt1 - mdpt2)
        self.queue.append(dist)
        if self.isIncreasing():
            self.action("zoomOut")
        elif self.isDecreasing():
            self.action("zoomIn")
        print(dist)
        #print(self.in_bounds(mdpt1), self.in_bounds(mdpt2))

    def isIncreasing(self, min_len=10):
        increase = 0
        queue = list(self.queue)
        if len(queue) < min_len:
            return False
        for i in range(1, len(queue)):
            if queue[i-1] < queue[i]:
                increase += 1

        if increase > min_len // 2:
            # reset queue
            self.queue.clear()
            return True
        return False

    def isDecreasing(self, min_len=10):
        decrease = 0
        queue = list(self.queue)
        if len(queue) < min_len:
            return False
        for i in range(1, len(queue)):
            if queue[i-1] > queue[i]:
                decrease += 1

        if decrease > min_len // 2:
            # reset queue
            self.queue.clear()
            return True
        return False

    def midpoint(self, box):
        return np.mean([[box[0], box[2]], [box[1], box[3]]], axis=1)
