from detector import Detector
from PIL import Image
import cv2
import io
import json
import serial


def capture_image():
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)  # width=640
    cap.set(4, 480)  # height=480

    if cap.isOpened():
        _, frame = cap.read()
        cap.release()  # releasing camera immediately after capturing picture
        if _ and frame is not None:
            cv2.imwrite('img.jpg', frame)


'''detectors = {
    'detector_1': Detector(weights='best_New_data_1_2.pth', cfg='models/yolov4-csp.yaml',
                           # classes=[0, 1, 4]
                           )
    #'detector_2': Detector('exp3_best_New_data.pth', cfg='models/yolov4-csp.yaml')
}

# lecture et conversion de l'image en bytes
im = Image.open('../4.jpeg')
im_resize = im.resize((500, 500))
buf = io.BytesIO()
im_resize.save(buf, format='JPEG')
byte_im = buf.getvalue()

print(json.dumps(detectors["detector_1"].detect(image=byte_im)))'''


'''serialPort = serial.Serial("/dev/ttyUSB0", baudrate=115200, timeout=1.0)
if(serialPort.isOpen() == False):
        serialPort.open()
while(True):
    print("waiting...\n")
    serialString = serialPort.readline()
    serialString = serialString.decode('Ascii')
    if(serialString != ""):
        capture_image()
    print(serialString)'''