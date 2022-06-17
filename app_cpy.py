import json
import os
import uuid
import io
import cv2
from PIL import Image
import requests
import numpy as np
import time
from utils.datasets import letterbox

from flask import Flask, jsonify, request, g, make_response
from werkzeug.utils import secure_filename

from detector import Detector
import sys

app = Flask(__name__)

#https://gist.github.com/andres-fr/f9c0d5993d7e7b36e838744291c26dde

@app.route('/send', methods=['POST'])
def send():
    img = cv2.imread('70.jpeg')

    img_size = 736
    img_resized = letterbox(np.array(img), new_shape=(img_size, img_size))[0]
    print(img.dtype)
    print(img_resized.shape)
    # convert numpy array to PIL Image
    '''ii = Image.fromarray(img)
    # create file-object in memory
    file_object = io.BytesIO()

    # write jpeg in file-object
    ii.save(file_object, 'jpeg', quality=100, subsampling=0)
    # move to beginning of file so `send_file()` it will read from start
    file_object.seek(0)'''

    t1 = time.time()


    resp = requests.post("http://127.0.0.1:5000/predict",
                         json={"file": img_resized.tolist(),
                               'detector': 'detector_1'
                                },
                         #files={'file': file_object},
                         #data={'detector': 'detector_1'}
                         )
    t2 = time.time()
    print(t2-t1)
    return make_response('0')


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        #file = request.files['file']
        file = request.json['file']
        #img_bytes = file.read()
        #image = Image.open(io.BytesIO(img_bytes))  # TODO a peut etre convertir en numpy
        #image_np = np.array(image)
        image_np = np.array(file)
        print(image_np[:10, 0, 0])

        img_origin = cv2.imread('70.jpeg')
        img_size = 736
        img_origin_resized = letterbox(np.array(img_origin), new_shape=(img_size, img_size))[0]
        print(img_origin_resized[:10, 0, 0])
        print(np.allclose(image_np, img_origin_resized))

    return make_response('0')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
