import json

from flask import Flask, jsonify, request
from detector import Detector


app = Flask(__name__)
detectors = {
    'detector_1': Detector(weights='best_New_data_1_2.pth', cfg='models/yolov4-csp.yaml')
    # 'detector_2': Detector(weights=d autres poids, cfg='models/un autre model ou le meme')
}


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        file = request.files['file']
        detector = request.detector
        img_bytes = file.read()
        return detectors[detector].detect(image=img_bytes)


if __name__ == '__main__':
    app.run()
