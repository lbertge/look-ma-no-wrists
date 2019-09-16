import sys
sys.path.append("pytorch_ssd/")
from pytorch_ssd.vision.ssd.mobilenetv1_ssd import create_mobilenetv1_ssd, create_mobilenetv1_ssd_predictor
import cv2
sys.path.insert(0, 'imagezmq/imagezmq')
import imagezmq
import numpy as np


top_k = 2
threshold = 0.7

def predict(image):
    net = create_mobilenetv1_ssd(top_k, is_test=True)
    predictor = create_mobilenetv1_ssd_predictor(net, candidate_size=200)

    boxes, labels, probs = predictor.predict(image, top_k, threshold)
    if boxes.size(0) > 0:
        return boxes, labels, probs
    return None

if __name__ == '__main__':
    image_hub = imagezmq.ImageHub()
    while True:
        image_name, image = image_hub.recv_image()
        out = predict(image)
        image_hub.send_reply(out)


