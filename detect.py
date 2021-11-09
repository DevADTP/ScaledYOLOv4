import argparse
import os
import platform
import shutil
import time
from pathlib import Path

import cv2
import torch
import torch.backends.cudnn as cudnn
from numpy import random

from models.yolo import Model
from models.experimental import attempt_load
from utils.datasets import LoadStreams, LoadImages
from utils.general import (
    check_img_size, non_max_suppression, apply_classifier, scale_coords, xyxy2xywh, plot_one_box, strip_optimizer)
from utils.torch_utils import select_device, load_classifier, time_synchronized

from IHM.package import conforme
import serial

import json
import paho.mqtt.client as mqtt

broker_adress = "127.0.0.1"
client = mqtt.Client("P1")
client.connect(broker_adress)
dict_pred={}
trame={"loc":"ESAT MENOGE","poste":1,"qrcode":"BBV59480A","quantity":60}
tab_fiches = ["BBV59480A.txt", "CCV59480A.txt"]

def Merge(dict1, dict2):
    # function that merges two dict (changes made in dict2)
    return(dict2.update(dict1))

def detect(save_img=False):

    out, source, weights, view_img, save_txt, imgsz, cfg = \
        opt.output, opt.source, opt.weights, opt.view_img, opt.save_txt, opt.img_size, opt.cfg
    webcam = source == '0' or source.startswith('rtsp') or source.startswith('http') or source.endswith('.txt')

    # Initialize
    device = select_device(opt.device)
    if os.path.exists(out):
        shutil.rmtree(out)  # delete output folder
    os.makedirs(out)  # make new output folder
    half = device.type != 'cpu'  # half precision only supported on CUDA

    # Load model
    if cfg == '':
        model = attempt_load(weights, map_location=device)  # load FP32 model
    else:
        import yaml  # for torch hub
        # yaml_file = Path(cfg).name
        with open(cfg) as f:
            yaml = yaml.load(f, Loader=yaml.FullLoader)  # model dict
        nc = yaml['nc']
        model = Model(opt.cfg, ch=3, nc=nc)
        weights_dict = torch.load(weights[0], map_location=device)
        model.load_state_dict(weights_dict)
        model.to(device)
        model.eval()
    imgsz = check_img_size(imgsz, s=model.stride.max())  # check img_size
    if half:
        model.half()  # to FP16

    # Second-stage classifier
    classify = False
    if classify:
        modelc = load_classifier(name='resnet101', n=2)  # initialize
        modelc.load_state_dict(torch.load('weights/resnet101.pt', map_location=device)['model'])  # load weights
        modelc.to(device).eval()

    # Set Dataloader
    vid_path, vid_writer = None, None
    if webcam:
        view_img = True
        cudnn.benchmark = True  # set True to speed up constant image size inference
        dataset = LoadStreams(source, img_size=imgsz)
    else:
        save_img = True
        dataset = LoadImages(source, img_size=imgsz)

    # Get names and colors
    if hasattr(model, 'module'):
        names = model.module.names
    elif hasattr(model, 'names'):
        names = model.names
    else:
        import yaml  # for torch hub
        # yaml_file = Path(cfg).name
        with open('data/adtp.yaml') as f:
            yaml = yaml.load(f, Loader=yaml.FullLoader)  # model dict
        names = yaml['names']
    colors = [[random.randint(0, 255) for _ in range(3)] for _ in range(len(names))]


    conforme.init_conform(dict_pred, tab_fiches[0])

    # Run inference
    t0 = time.time()
    img = torch.zeros((1, 3, imgsz, imgsz), device=device)  # init img
    _ = model(img.half() if half else img) if device.type != 'cpu' else None  # run once
    for path, img, im0s, vid_cap in dataset:
        img = torch.from_numpy(img).to(device)
        img = img.half() if half else img.float()  # uint8 to fp16/32
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        # Inference
        t1 = time_synchronized()
        pred = model(img, augment=opt.augment)[0]

        # Apply NMS
        pred = non_max_suppression(pred, opt.conf_thres, opt.iou_thres, classes=opt.classes, agnostic=opt.agnostic_nms)
        t2 = time_synchronized()

        # Apply Classifier
        if classify:
            pred = apply_classifier(pred, modelc, img, im0s)

        # Process detections
        for i, det in enumerate(pred):  # detections per image
            if webcam:  # batch_size >= 1
                p, s, im0 = path[i], '%g: ' % i, im0s[i].copy()
            else:
                p, s, im0 = path, '', im0s

            save_path = str(Path(out) / Path(p).name)
            txt_path = str(Path(out) / Path(p).stem) + ('_%g' % dataset.frame if dataset.mode == 'video' else '')
            s += '%gx%g ' % img.shape[2:]  # print string
            s_tmp = s
            gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
            #time.sleep(1.5)
            serialString = serialPort.readline()

            global nom  # nom du chicher de la fiche scanné
            try:
                nom
            except NameError:
                nom = tab_fiches[0]  # fiche par défaut lors du lancement du programme

            if (serialString.decode('Ascii') != "" ):
                #time.sleep(1)
                serialString = serialString.decode('Ascii')
                serialString = serialString[0:len(serialString) - 1]
                serialString = serialString + ".txt"
                conforme.init_conform(dict_pred, serialString)
                if (os.path.exists(serialString) and serialString in tab_fiches):
                    nom = serialString

            print("\n--------------------------------\n")
            print("fiche utilisée : " + nom)
            

            if det is None:
                conforme.not_detected(serialPort)
            if det is not None and len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()
                # Print results
                for c in det[:, -1].unique():
                    n = (det[:, -1] == c).sum()  # detections per class
                    s += '%g %ss, ' % (n, names[int(c)])  # add to string
                    dict_pred[names[int(c)]] = [n.item()]

                valide = conforme.conformite_conditionnement_dict(dict_pred,nom, serialPort)

                #Mise en forme de la trame pour envoie vers le broker
                copie_dict_pred = dict_pred.copy()
                #conversion des valeur de tableau à integer
                for key, value in copie_dict_pred.items():
                    copie_dict_pred[key] = value[0]
				
                dict_quantity = conforme.get_dict_quantity(dict_pred)
                trame = {"loc": "ESAT MENOGE", "poste": 1, "qrcode": nom, "quantity": 60 , "valide":valide}
                Merge(dict_quantity,trame)
                trame = json.dumps(trame)
                client.publish("IA_inference_poste1", trame)


                for key in dict_pred:
                    dict_pred[key].pop()

                # Write results

                for *xyxy, conf, cls in det:
                    if save_txt:  # Write to file
                        xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh
                        with open(txt_path + '.txt', 'a') as f:
                            f.write(('%g ' * 5 + '\n') % (cls, *xywh))  # label format

                    if save_img or view_img:  # Add bbox to image
                        label = '%s' % (names[int(cls)])
                        plot_one_box(xyxy, im0, label=label, color=colors[int(cls)], line_thickness=2)

            # Print time (inference + NMS)
            #time.sleep(1.5)
            #print('%sDone. (%.3fs)' % (s, t2 - t1))
            print("pièces detectées : " + s[11:len(s)])
            print("\n--------------------------------\n")
            # Stream results
            if view_img:
                cv2.imshow(p, im0)

                if cv2.waitKey(1) == ord('q'):  # q to quit
                    serialPort.close()
                    raise StopIteration

            # Save results (image with detections)
            if save_img:
                if dataset.mode == 'images':
                    cv2.imwrite(save_path, im0)
                else:
                    if vid_path != save_path:  # new video
                        vid_path = save_path
                        if isinstance(vid_writer, cv2.VideoWriter):
                            vid_writer.release()  # release previous video writer

                        fourcc = 'mp4v'  # output video codec
                        fps = vid_cap.get(cv2.CAP_PROP_FPS)
                        w = int(vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                        h = int(vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                        vid_writer = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*fourcc), fps, (w, h))
                    vid_writer.write(im0)

    if save_txt or save_img:
        print('Results saved to %s' % Path(out))
        if platform == 'darwin' and not opt.update:  # MacOS
            os.system('open ' + save_path)

    print('Done. (%.3fs)' % (time.time() - t0))


if __name__ == '__main__':
    serialPort = serial.Serial("/dev/ttyUSB0", baudrate=115200, timeout=1.0)
    if(serialPort.isOpen() == False):
       serialPort.open()

    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', nargs='+', type=str, default='yolov4-p5.pt', help='model.pt path(s)')
    parser.add_argument('--source', type=str, default='0', help='source')  # file/folder, 0 for webcam
    parser.add_argument('--output', type=str, default='inference/output', help='output folder')  # output folder
    parser.add_argument('--img-size', type=int, default=736, help='inference size (pixels)')
    parser.add_argument('--conf-thres', type=float, default=0.7, help='object confidence threshold')
    parser.add_argument('--iou-thres', type=float, default=0.5, help='IOU threshold for NMS')
    parser.add_argument('--device', default='', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
    parser.add_argument('--view-img', action='store_true', help='display results')
    parser.add_argument('--save-txt', action='store_true', help='save results to *.txt')
    parser.add_argument('--classes', nargs='+', type=int, help='filter by class: --class 0, or --class 0 2 3')
    parser.add_argument('--agnostic-nms', action='store_true', help='class-agnostic NMS')
    parser.add_argument('--augment', action='store_true', help='augmented inference')
    parser.add_argument('--update', action='store_true', help='update all models')
    parser.add_argument('--cfg', type=str, default='models/yolov4-csp.yaml', help='model.yaml path')
    opt = parser.parse_args()
    print(opt)
    
    #print("-------------------------------")
    #print(tab_predictions)
    #print("-------------------------------")
	
    with torch.no_grad():
        if opt.update:  # update all models (to fix SourceChangeWarning)
            for opt.weights in ['']:
                detect()
                strip_optimizer(opt.weights)
        else:
            detect()
