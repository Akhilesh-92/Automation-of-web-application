import requests
import json
import pytest

#  Login to app using api
def test_valid_login():
	payload = {"username": "jsmith","password": "demo1234"}
	res = requests.post(url="https://demo.testfire.net/api/login", json=payload, verify=False)
	if res.status_code == 200:
		print("connection success")
	data = json.loads(res.content)
	print(data)
	assert res.status_code == 200
	assert data['Authorization'] != None

