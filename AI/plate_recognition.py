from yolov6.layers.common import DetectBackend
from yolov6.data.data_augment import letterbox
from yolov6.utils.nms import non_max_suppression


import torch
import cv2
import numpy as np
import os
import math

class PlateRecognition:
    def __init__(self):

        self.__dict__.update(locals())

        WORKING_DIR = os.getcwd()
        WEIGHTS = WORKING_DIR + '/plate_recognition.pt'

        self.model = DetectBackend(WEIGHTS, device='cpu')
        self.stride = self.model.stride
        self.img_size=640
        self.img_size = self.check_img_size(self.img_size, s=self.stride)
        self.half = False
        


    def getPlate(self, input_image):
        img = letterbox(input_image, self.img_size, stride=self.stride)[0]
        img = img.transpose((2, 0, 1))[::-1]  # HWC to CHW, BGR to RGB
        img = torch.from_numpy(np.ascontiguousarray(img))
        img = img.half() if self.half else img.float()  # uint8 to fp16/32
        img /= 255  # 0 - 255 to 0.0 - 1.0

        if len(img.shape) == 3:
                img = img[None]

        conf_thres=0.4
        iou_thres=0.45
        max_det=1000
        classes=None
        agnostic_nms=False
        pred_results = self.model(img)
        det = non_max_suppression(pred_results, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)[0]

        if len(det):
            det[:, :4] = self.rescale(img.shape[2:], det[:, :4], input_image.shape).round()
            max_conf = 0
            max_conf_xyxy = None

            for *xyxy, conf, cls in reversed(det):
                if conf > max_conf:
                    max_conf = conf
                    max_conf_xyxy = xyxy

            if max_conf_xyxy is not None:
                return input_image[int(max_conf_xyxy[1]):int(max_conf_xyxy[3]), int(max_conf_xyxy[0]):int(max_conf_xyxy[2])]

        return None


    def check_img_size(self, img_size, s=32, floor=0):
        """Make sure image size is a multiple of stride s in each dimension, and return a new shape list of image."""
        if isinstance(img_size, int):  # integer i.e. img_size=640
            new_size = max(self.make_divisible(img_size, int(s)), floor)
        elif isinstance(img_size, list):  # list i.e. img_size=[640, 480]
            new_size = [max(self.make_divisible(x, int(s)), floor) for x in img_size]
        else:
            raise Exception(f"Unsupported type of img_size: {type(img_size)}")

        if new_size != img_size:
            print(f'WARNING: --img-size {img_size} must be multiple of max stride {s}, updating to {new_size}')
        return new_size if isinstance(img_size,list) else [new_size]*2

    def make_divisible(self, x, divisor):
        # Upward revision the value x to make it evenly divisible by the divisor.
        return math.ceil(x / divisor) * divisor
    
    @staticmethod
    def rescale(ori_shape, boxes, target_shape):
        '''Rescale the output to the original image shape'''
        ratio = min(ori_shape[0] / target_shape[0], ori_shape[1] / target_shape[1])
        padding = (ori_shape[1] - target_shape[1] * ratio) / 2, (ori_shape[0] - target_shape[0] * ratio) / 2

        boxes[:, [0, 2]] -= padding[0]
        boxes[:, [1, 3]] -= padding[1]
        boxes[:, :4] /= ratio

        boxes[:, 0].clamp_(0, target_shape[1])  # x1
        boxes[:, 1].clamp_(0, target_shape[0])  # y1
        boxes[:, 2].clamp_(0, target_shape[1])  # x2
        boxes[:, 3].clamp_(0, target_shape[0])  # y2

        return boxes