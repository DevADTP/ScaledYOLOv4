import requests

resp = requests.post("http://localhost:5000/predict",
                     files={"file": open('../70.jpeg', 'rb'),
                            },
                     data={'detector': 'detector_1'}
                     )

print(resp.json())
