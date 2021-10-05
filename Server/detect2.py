import argparse
import os
import platform
import shutil
import time
from pathlib import Path
import numpy
import cv2
import torch
import torch.backends.cudnn as cudnn
from numpy import random
import threading
import pymysql

from models.experimental import attempt_load
from utils.datasets import LoadStreams, LoadImages
from utils.general import (
    check_img_size, non_max_suppression, apply_classifier, scale_coords,
    xyxy2xywh, plot_one_box, strip_optimizer, set_logging)
from utils.torch_utils import select_device, load_classifier, time_synchronized
import socket

#connect = pymysql.connect(host = "113.198.234.48", user = 'test2', password = '1', db = 'test', charset = 'utf8')

def letterbox(img, new_shape=(640, 640), color=(114, 114, 114), auto=True, scaleFill=False, scaleup=True):
    # Resize image to a 32-pixel-multiple rectangle https://github.com/ultralytics/yolov3/issues/232
    shape = img.shape[:2]  # current shape [height, width]
    if isinstance(new_shape, int):
        new_shape = (new_shape, new_shape)

    # Scale ratio (new / old)
    r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
    if not scaleup:  # only scale down, do not scale up (for better test mAP)
        r = min(r, 1.0)

    # Compute padding
    ratio = r, r  # width, height ratios
    new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
    dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]  # wh padding
    if auto:  # minimum rectangle
        dw, dh = numpy.mod(dw, 64), numpy.mod(dh, 64)  # wh padding
    elif scaleFill:  # stretch
        dw, dh = 0.0, 0.0
        new_unpad = (new_shape[1], new_shape[0])
        ratio = new_shape[1] / shape[1], new_shape[0] / shape[0]  # width, height ratios

    dw /= 2  # divide padding into 2 sides
    dh /= 2

    if shape[::-1] != new_unpad:  # resize
        img = cv2.resize(img, new_unpad, interpolation=cv2.INTER_LINEAR)
    top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
    left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
    img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)  # add border
    return img, ratio, (dw, dh)


def detect(source):
    out, weights, imgsz = \
        'inference/images', 'yolov5x.pt', 640
    import carnumber
    try:
        carnumber_img ,carnumber_text= carnumber.carnumber_feature(source)
    except:
        print("차량번호판 인식 실패 ")
        carnumber_img, carnumber_text = "",""
    # Initialize
    set_logging()
    device = select_device('')
    if os.path.exists(out):
        shutil.rmtree(out)  # delete output folder
    os.makedirs(out)  # make new output folder
    half = device.type != 'cpu'  # half precision only supported on CUDA

    # Load model
    model = attempt_load(weights, map_location=device)  # load FP32 model
    imgsz = check_img_size(imgsz, s=model.stride.max())  # check img_size
    if half:
        model.half()  # to FP16

    names = model.module.names if hasattr(model, 'module') else model.names

    if True:
        if True:
            # Padded resize
            img = letterbox(source, new_shape=640)[0]

            # Convert
            img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
            img = numpy.ascontiguousarray(img)

            img = torch.from_numpy(img).to(device)
            img = img.half() if half else img.float()  # uint8 to fp16/32
            img /= 255.0  # 0 - 255 to 0.0 - 1.0
            if img.ndimension() == 3:
                img = img.unsqueeze(0)

            pred = model(img, augment=False)[0]

            # Apply NMS
            pred = non_max_suppression(pred, 0.4, 0.2, classes=False, agnostic=False)
            #class_text = ""

            # Process detections
            for i, det in enumerate(pred):  # detections per image
                p, s, im0 = '', '', source

                gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
                if det is not None and len(det):
                    # Rescale boxes from img_size to im0 size
                    det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()

                    # Print results
                    for c in det[:, -1].unique():
                        n = (det[:, -1] == c).sum()  # detections per class
                        s += '%g %ss,' % ( n ,names[int(c)])  # add to string

               #return s,carnumber_text, carnumber_img,im0
            return s, carnumber_text
            '''
            cur = connect.cursor()
            sql2 = "select * from ligal_carnumber where carnumber = '" + carnumber_text + "' "
            cur.execute(sql2)
            row = cur.fetchall()
            #print(str(row))
            if row:
                print("저장된 장애인차량입니다.")
            else:
                print("시작")
                sql = "insert into illegal_carnumber values(" + "'" + carnumber_text + "', 500000 , '" + LOAD_FILE(source) + "')"
                cur.execute(sql)
                print("데이터 삽입 완료")
                connect.commit()
            print('asdasdasdsadsad"')
            import time
            if carnumber_text == 0 and carnumber_img == 0:
                return class_text, source ,time.strftime('%c', time.localtime(time.time())) # 클래스 정보 , 사진 , 시간
            else:
                return carnumber_text,carnumber_img,source, time.strftime('%c', time.localtime(time.time())) # 차량번호판 string , 차량번호판 이미지 , 사진
            '''
            #cv2.imshow('ImageWindow', im0)
            #cv2.imshow('ImageWindow', carnumber_img)
            #cv2.waitKey(1)

    #client_socket.close()
    #connect.close()



