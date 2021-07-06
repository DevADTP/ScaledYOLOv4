import requests

resp = requests.post("http://localhost:5000/predict",
                     files={"file": open('../106.jpg', 'rb')},
                     detector='detector_1'
                     )

print(resp.json())
