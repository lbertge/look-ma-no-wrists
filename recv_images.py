import sys
sys.path.append("pytorch_ssd/")
from pytorch_ssd.vision.ssd.mobilenetv1_ssd import create_mobilenetv1_ssd, create_mobilenetv1_ssd_predictor
import cv2
sys.path.insert(0, 'imagezmq/imagezmq')
import imagezmq
import numpy as np
import argparse
import zmqnumpy

top_k = 2
threshold = 0.7

if __name__ == '__main__':
    image_hub = imagezmq.ImageHub()
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_path', dest='model_path', type=str, help="Trained model path", required=True)
    args = parser.parse_args()

    net = create_mobilenetv1_ssd(top_k, is_test=True)
    predictor = create_mobilenetv1_ssd_predictor(net, candidate_size=200)

    net.load(args.model_path)

    while True:
        image_name, image = image_hub.recv_image()
        boxes, labels, probs = predictor.predict(image, top_k, threshold)
        if boxes.size(0) > 0:
            loc = [boxes[i, :].numpy() for i in range(boxes.size(0))]
            image_hub.send_reply(np.array(loc))
        else:
            image_hub.send_reply(b'')


