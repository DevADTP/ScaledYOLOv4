import requests

resp = requests.post("http://localhost:5000/predict",
                     files={"file": open('../106.jpg','rb')})

print(resp.json())