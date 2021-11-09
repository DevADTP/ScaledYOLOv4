import requests

resp = requests.post("http://192.168.72.118:5000/predict",
                     files={"file": open('../NewPicture.jpg', 'rb'),
                            },
                     data={'detector': 'detector_1'}
                     )

print(resp.json())