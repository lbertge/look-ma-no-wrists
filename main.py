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
from bounds import draw_bounds
from manager import CommandManager
sys.path.append("/Users/albertge/tonystark/pytorch_ssd/")
from pytorch_ssd.vision.ssd.mobilenetv1_ssd import create_mobilenetv1_ssd, create_mobilenetv1_ssd_predictor
from pytorch_ssd.vision.ssd.mobilenet_v2_ssd_lite import create_mobilenetv2_ssd_lite, create_mobilenetv2_ssd_lite_predictor

frame_processed = 0
threshold = 0.7

top_k = 2

def worker(input_q, output_q, cap_params, frame_processed):
    # ignore SIGINT, let parent process handle
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    #net
    if cap_params['net_type'] == "mb1-ssd":
        net = create_mobilenetv1_ssd(top_k, is_test=True)
    elif cap_params['net_type'] == "mb2-ssd-lite":
        net = create_mobilenetv2_ssd_lite(top_k, is_test=True)
    else:
        raise NotImplementedError

    net.load(cap_params['model_path'])

    if cap_params['net_type'] == "mb1-ssd":
        predictor = create_mobilenetv1_ssd_predictor(net, candidate_size=200)
    elif cap_params['net_type'] == "mb2-ssd-lite":
        predictor = create_mobilenetv2_ssd_lite_predictor(net, candidate_size=200)
    else:
        raise NotImplementedError

    while True:
        image = input_q.get()
        if (image is not None):
            boxes, labels, probs = predictor.predict(image, top_k, threshold)
            if boxes.size(0) > 0:
                loc = [boxes[i, :] for i in range(boxes.size(0))]

                output_q.put((loc, probs))
            else:
                output_q.put(None)

        else:
            output_q.put(frame)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--src', dest='video_source', type=int, default=0, help='Device index of camera')
    parser.add_argument('--nhands', dest='num_hands', type=int, default=2, help='Max number of hands to detect')
    parser.add_argument('--fps', dest='fps', type=int, default=0, help='Show FPS on detection')
    parser.add_argument('--width', dest='width', type=int, default=300, help='Width of the frame of video stream')
    parser.add_argument('--height', dest='height', type=int, default=200, help='Height of the frame of video stream')
    parser.add_argument('--num_workers', dest='num_workers', type=int, default=4, help='Number of workers for multiprocessing')
    parser.add_argument('--queue-size', dest='queue_size', type=int, default=5, help='Size of the multiprocessing queue')
    parser.add_argument('--net_type', dest='net_type', type=str, default='mb1-ssd', help='SSD network type',
        choices=["mb1-ssd", "mb2-ssd-lite"])
    parser.add_argument('--model_path', dest='model_path', type=str, help="Trained model path", required=True)
    parser.add_argument('--display', dest='display', type=bool, default=False, help="Display boxes")

    args = parser.parse_args()

    input_q = Queue(maxsize=args.queue_size)
    output_q = Queue(maxsize=args.queue_size)

    video_capture = WebcamVideoStream(src=args.video_source, width=args.width, height=args.height).start()

    cap_params = {}
    frame_processed = 0
    cap_params['im_width'], cap_params['im_height'] = video_capture.size()
    cap_params['threshold'] = threshold
    cap_params['num_hands'] = args.num_hands
    cap_params['net_type'] = args.net_type
    cap_params['model_path'] = args.model_path

    print(cap_params, args)

    pool = Pool(args.num_workers, worker, (input_q, output_q, cap_params, frame_processed))

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

            input_q.put(image)
            try:
                out = output_q.get()
            except q.Empty:
                continue

            #elapsed_time = (datetime.datetime.now() - start_time).total_seconds()
            num_frames += 1
            #fps = num_frames / elapsed_time

            if args.display > 0:
                if (out is not None):
                    loc, probs = out
                    for box in loc:
                        cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (255, 255, 0), 4)
                    manager.recv_boxes(loc)
                draw_bounds(frame)
                cv2.imshow('annotated', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                if (out is not None):
                    loc, probs = out
                    # activated
                    #print(f"Detected hands at {out}")
                    manager.recv_boxes(loc)

    except KeyboardInterrupt:
        pass

    elapsed_time = (datetime.datetime.now() - start_time).total_seconds()
    fps = num_frames / elapsed_time
    print("fps", fps)
    pool.close()
    pool.terminate()
    print("processes terminated")
    video_capture.stop()
    print("video terminated")
    cv2.destroyAllWindows()
    print("windows terminated")
    #os.kill(os.getpid(), 9)
        
