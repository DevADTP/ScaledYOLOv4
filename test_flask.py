import requests

resp = requests.post("http://localhost:5000/predict",
                     files={"file": open('../101.jpeg', 'rb'),
                            },
                     data={'detector': 'detector_1'}
                     )

print(resp.json())
