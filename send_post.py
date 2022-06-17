import requests
import time 

t1 = time.time()
requests.post("http://127.0.0.1:5000/send")
t2=time.time()
print(t2-t1)

