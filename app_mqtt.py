import json
from detector import Detector
import paho.mqtt.client as mqtt

broker_adress="127.0.0.1"
client=mqtt.Client("P1")
client.connect(broker_adress)

'''detectors = {
    'detector_1': Detector(weights='best_improve.pth', cfg='models/yolov4-csp.yaml',
                           # classes=[0, 1, 4]
                           )

    #'detector_2': Detector('exp3_best_New_data.pth', cfg='models/yolov4-csp.yaml')
}'''

def predict():
    file = open('../a13.jpeg', 'rb')
    img_bytes = file.read()
    return detectors['detector_1'].detect(image=img_bytes)


if __name__ == '__main__':
    trame = predict()
    trame = json.dumps(trame)
    print(trame)
    client.publish("test",trame)