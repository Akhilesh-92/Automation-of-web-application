import pytest
import requests
import json


#  Login to app using api
payload = {"username": "jsmith","password": "demo1234"}
res = requests.post(url="https://demo.testfire.net/api/login", json=payload, verify=False)
data = json.loads(res.content)
headers = {'Authorization': data['Authorization']}
def test_valid_login():
	assert res.status_code == 200
	assert data['Authorization'] != None

def account_info():
	account_res = requests.get(url='http://demo.testfire.net/api/account', headers=headers)
	account_info = json.loads(account_res.content)
	return account_info

#  Get the savings account details using api
def test_Account_info():
	acc_info = account_info()
	assert acc_info['Accounts'][0]['Name'] == 'Savings'
	assert acc_info['Accounts'][1]['Name'] == 'Checking'
	assert acc_info['Accounts'][2]['Name'] == 'Credit Card'


def test_get_savings_id():
	acc_info = account_info()
	for ele in acc_info['Accounts']:
		if ele['Name'] == "Savings":
			acc_id = ele['id']
	assert acc_id == "800002"


# Find the last 10 transactions using api
def last_ten_transactions():
	acc_info = account_info()
	url = 'http://demo.testfire.net/api/account'+ '/' + acc_info['Accounts'][0]['id'] + '/' + 'transactions'
	trans = requests.get(url=url, headers=headers)
	last_ten_trans = json.loads(trans.content)
	return last_ten_trans

def test_trans():
	last_trans = last_ten_transactions()
	assert last_trans['last_10_transactions'][0]['date'] == "2021-04-16"


# Check if there is a transaction above 500$
def test_transfer_Amount():
	last_trans = last_ten_transactions()
	for items in last_trans['last_10_transactions']:
		# If so transfer 100$ to some account using api
		if float(items['ammount'].replace('$','')) > 5.00:
			payload2 = {
				  "toAccount": "800003",
				  "fromAccount": "800002",
				  "transferAmount": "100"
			}

			res2 = requests.post(url="https://demo.testfire.net/api/transfer", headers = headers, json=payload2, verify=False)
			data2 = json.loads(res2.content)
			print(data2)
			break
	assert data2['success'] != ""
