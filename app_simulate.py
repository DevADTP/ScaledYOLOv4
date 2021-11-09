import json

from flask import Flask, jsonify, request
from detector import Detector


app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        file = request.files['file']
        # print(request.form)
        detector = request.form['detector']
        img_bytes = file.read()
        return jsonify({'Rondelle': [3],'Capuchon_Plastique' : [4]})


if __name__ == '__main__':
    app.run(host='0.0.0.0')
