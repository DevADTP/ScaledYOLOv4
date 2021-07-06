import argparse
import os
import platform
import shutil
import time
from pathlib import Path
import io

import cv2
import torch
import torchvision.transforms as transforms
import torch.backends.cudnn as cudnn
from numpy import random
import numpy as np

import yaml

from PIL import Image

from models.yolo import Model
from models.experimental import attempt_load
from utils.datasets import LoadStreams, LoadImages, letterbox
from utils.general import (
    check_img_size, non_max_suppression, apply_classifier, scale_coords, xyxy2xywh, plot_one_box, strip_optimizer)
from utils.torch_utils import select_device, load_classifier, time_synchronized

import json


class Detector(object):

    def __init__(self, weights='best_New_data_1_2.pth', img_size=640, conf_thres=0.4,
                 iou_thres=0.5, classes=None, agnostic_nms=True, cfg='models/yolov4-csp.yaml'):
        weight_path = '../weights/Trainings/Must/'
        self.weights = os.path.join(weight_path, weights)

        self.conf_thres = conf_thres
        self.img_size = img_size
        self.iou_thres = iou_thres
        self.agnostic_nms = agnostic_nms
        self.cfg = cfg
        self.classes = [0, 1, 2, 3, 4] if classes is None else classes
        assert isinstance(self.classes, list), 'We must have at least 2 classes, self.classes must be a list'

        self.device = select_device('')
        #self.device = 'cuda:0' if torch.cuda.is_available() else 'cpu'

        # Load model
        if cfg == '':
            self.model = attempt_load(self.weights, map_location=self.device)  # load FP32 model
        else:
            with open(cfg) as f:
                yaml_f = yaml.load(f, Loader=yaml.FullLoader)  # model dict
            nc = yaml_f['nc']
            self.model = Model(cfg, ch=3, nc=nc)
            weights_dict = torch.load(self.weights, map_location=self.device)
            self.model.load_state_dict(weights_dict)
            print('weights loaded')
            self.model.to(self.device)
            self.model.eval()

    def prepare_image(self, image_bytes):

        image = Image.open(io.BytesIO(image_bytes))  # TODO a peut etre convertir en numpy
        image = transforms.ToTensor()(letterbox(np.array(image), new_shape=(self.img_size, self.img_size))[0])
        # Convert
        image = image.to(self.device)
        return image.unsqueeze(0)

    def detect(self, image):

        image = self.prepare_image(image)
        with open('data/adtp.yaml') as f:
            yaml_f = yaml.load(f, Loader=yaml.FullLoader)  # model dict
        names = yaml_f['names']

        # Run inference
        pred = self.model(image, augment=False)[0].detach().to('cpu')

        # Apply NMS
        pred = non_max_suppression(pred, self.conf_thres, self.iou_thres, classes=self.classes,
                                   agnostic=self.agnostic_nms)

        # Process detections
        data_json = json.dumps({})
        dict_pred = {}
        for i, det in enumerate(pred):  # detections per image

            if det is not None and len(det):
                # print('######## det #########')
                # print(det)
                # Print results
                for c in det[:, -1].unique():
                    n = (det[:, -1] == c).sum()  # detections per class
                    dict_pred[names[int(c)]] = [n.item()]

                # data_json = json.dumps(dict_pred, sort_keys=True, indent=4, separators=(',', ': '))

        return dict_pred

        # return data_json
