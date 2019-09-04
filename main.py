import cv2
import multiprocessing
from multiprocessing import Queue, Pool
import time
import datetime
from webcam import WebcamVideoStream
import argparse

frame_processed = 0
threshold = 0.4

top_k = 2

def worker(input_q, output_q, cap_params, frame_processed):
    #net
    net = init_net()

    while True:
        frame = input_q.get()
        if frame:
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            boxes, labels, probs = predictor.predict(image, top_k, threshold)
            if len(boxes.size(0)) > 0:
                loc = [boxes[i, :] for i in range(boxes.size(0))]

                output_q.put(loc)
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
    args = parser.parse_args()

    input_q = Queue(maxsize=args.queue_size)
    output_q = Queue(maxsize=args.queue_size)

    video_capture = WebcamVideoStream(src=args.video_source, width=args.width, height=args.height).start()

    cap_params = {}
    frame_processed = 0
    cap_params['im_width'], cap_params['im_height'] = video_capture.size()
    cap_params['threshold'] = threshold

    cap_params['num_hands'] = args.num_hands

    print(cap_params, args)

    pool = Pool(args.num_workers, worker, (input_q, output_q, cap_params, frame_processed))

    start_time = datetime.datetime.now()
    num_frame = 0
    fps = 0
    index = 0

    activated = False

    while True:
        frame = video_capture.read()
        frame = cv2.flip(frame, 1)
        index += 1

        input_q.put(frame)

        out = output_q.get()

        elapsed_time = (datetime.datetime.now() - start_time).total_seconds()
        num_frames += 1
        fps = num_frames / elapsed_time

        if out:
            # activated
            activated = True
            print(f"Detected hands at {out}")
        else:
            activated = False

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    elapsed_time = (datetime.datetime.now() - start_time).total_seconds()
    fps = num_frames / elapsed_time
    print("fps", fps)
    pool.terminate()
    video_capture.stop()
    cv2.destroyAllWindows()
        


        



