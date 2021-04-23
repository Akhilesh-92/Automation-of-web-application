import requests
import json
import pytest

#  Login to app using api
# def valid_login():
payload = {"username": "jsmith","password": "demo1234"}
res = requests.post(url="https://testfire.net/api/login", json=payload, verify=False)
if res.status_code == 200:
	print("connection success")
# assert res.status_code == 200
data = json.loads(res.content)
print(data)
# assert type(data['Authorization']) == str

