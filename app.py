import json

from flask import Flask, jsonify, request
from detector import Detector


app = Flask(__name__)
detectors = {
    'detector_1': Detector(weights='best_New_data_1_2.pth', cfg='models/yolov4-csp.yaml',
                           # classes=[0, 1, 4]
                           )
    #'detector_2': Detector('exp3_best_New_data.pth', cfg='models/yolov4-csp.yaml')
}


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        file = request.files['file']
        # print(request.form)
        detector = request.form['detector']
        img_bytes = file.read()
        return jsonify(detectors[detector].detect(image=img_bytes))


if __name__ == '__main__':
    app.run(host='0.0.0.0')
