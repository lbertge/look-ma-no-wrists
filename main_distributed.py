import cv2
import multiprocessing
from multiprocessing import Queue, Pool
import time
import datetime
from webcam import WebcamVideoStream
import argparse
import sys
import signal
import queue as q
import os
import numpy as np
from send_images import ImageSender
from bounds import draw_bounds
from manager import CommandManager
# sys.path.append(os.getcwd() + "/pytorch_ssd/")
# from pytorch_ssd.vision.ssd.mobilenetv1_ssd import create_mobilenetv1_ssd, create_mobilenetv1_ssd_predictor
# from pytorch_ssd.vision.ssd.mobilenet_v2_ssd_lite import create_mobilenetv2_ssd_lite, create_mobilenetv2_ssd_lite_predictor

frame_processed = 0
threshold = 0.7

top_k = 2

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--src', dest='video_source', type=int, default=0, help='Device index of camera')
    parser.add_argument('--fps', dest='fps', type=int, default=0, help='Show FPS on detection')
    parser.add_argument('--width', dest='width', type=int, default=300, help='Width of the frame of video stream')
    parser.add_argument('--height', dest='height', type=int, default=200, help='Height of the frame of video stream')
    # parser.add_argument('--nhands', dest='num_hands', type=int, default=2, help='Max number of hands to detect')
    # parser.add_argument('--num_workers', dest='num_workers', type=int, default=4, help='Number of workers for multiprocessing')
    # parser.add_argument('--queue-size', dest='queue_size', type=int, default=5, help='Size of the multiprocessing queue')
    # parser.add_argument('--net_type', dest='net_type', type=str, default='mb1-ssd', help='SSD network type',
        # choices=["mb1-ssd", "mb2-ssd-lite"])
    # parser.add_argument('--model_path', dest='model_path', type=str, help="Trained model path", required=True)
    parser.add_argument('--display', dest='display', type=bool, default=False, help="Display boxes")

    args = parser.parse_args()

    video_capture = WebcamVideoStream(src=args.video_source, width=args.width, height=args.height).start()

    cap_params = {}
    frame_processed = 0
    cap_params['im_width'], cap_params['im_height'] = video_capture.size()
    cap_params['threshold'] = threshold

    print(cap_params, args)

    sender = ImageSender(connect_to='tcp://192.168.1.86:5555')

    start_time = datetime.datetime.now()
    num_frames = 0
    fps = 0
    index = 0

    manager = CommandManager()

    try:
        while True:
            frame = video_capture.read()
            frame = cv2.flip(frame, 1)
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            index += 1

            out = sender.send_image(image)

            #elapsed_time = (datetime.datetime.now() - start_time).total_seconds()
            num_frames += 1
            #fps = num_frames / elapsed_time

            if args.display > 0:
                if (out is not None):
                    loc = out
                    for box in loc:
                        box = list(map(int, box))
                        cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (255, 255, 0), 4)
                    manager.recv_boxes(loc)
                draw_bounds(frame)
                cv2.imshow('annotated', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                if (out is not None):
                    loc = out
                    # activated
                    #print(f"Detected hands at {out}")
                    manager.recv_boxes(loc)

    except KeyboardInterrupt:
        pass

    elapsed_time = (datetime.datetime.now() - start_time).total_seconds()
    fps = num_frames / elapsed_time
    print("fps", fps)
    video_capture.stop()
    print("video terminated")
    cv2.destroyAllWindows()
    print("windows terminated")
    #os.kill(os.getpid(), 9)
        
