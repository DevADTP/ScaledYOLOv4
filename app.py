import io
import json

from torchvision import models
import torchvision.transforms as transforms
from PIL import Image
from flask import Flask, jsonify, request
from detector import Detector


app = Flask(__name__)
imagenet_class_index = json.load(open('../imagenet_class_index.json'))
#detector_1 = Detector(weights='', cfg='')
detector_1 = Detector( weights='../weights/Trainings/Must/best_New_data_1_2.pth', cfg='models/yolov4-csp.yaml')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        file = request.files['file']
        img_bytes = file.read()
        return detector_1.detect(image=img_bytes)


if __name__ == '__main__':
    app.run()
