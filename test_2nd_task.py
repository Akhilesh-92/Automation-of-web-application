import requests
import json
import pytest

#  Login to app using api
payload = {"username": "jsmith","password": "demo1234"}
res = requests.post(url="http://demo.testfire.net/api/login", json=payload)
data = json.loads(res.content)
headers = {'Authorization': data['Authorization']}

def test_valid_login():
	assert res.status_code == 200
	assert data['Authorization'] != None


# Get all existing account types using api
def account_info():
	account_res = requests.get(url='http://demo.testfire.net/api/account', headers=headers)
	account = json.loads(account_res.content)
	return account

	
def test_account_info():
	acc_info = account_info()
	assert acc_info['Accounts'][0]['Name'] == 'Savings'
	assert acc_info['Accounts'][1]['Name'] == 'Checking'
	assert acc_info['Accounts'][2]['Name'] == 'Credit Card'
	


# Fetching the savings account details
def test_get_savings_details():
	acc_info = account_info()
	for ele in acc_info['Accounts']:
		if ele['Name'] == "Savings":
			acc_type = ele['Name']
			acc_id = ele['id']
	assert acc_id == '800002'


def test_fetch_balance():
	acc_info = account_info()
	url = 'http://demo.testfire.net/api/account'+ '/' + acc_info['Accounts'][0]['id']
	account_No = requests.get(url = url, headers= headers)
	acc_balance = json.loads(account_No.content)
	assert account_No.status_code == 200
	assert acc_balance['balance'] != ""


# Find the latest transaction using api
def latest_transactions():
	acc_info = account_info()
	url = 'http://demo.testfire.net/api/account'+ '/' + acc_info['Accounts'][0]['id'] + '/' + 'transactions'
	trans = requests.get(url = url, headers= headers)
	last_ten_trans = json.loads(trans.content)
	return last_ten_trans
	
def test_trans():
	last_trans = latest_transactions()
	assert last_trans['last_10_transactions'][0]['date'] == "2021-04-16"
	

# Fetch the date of the latest transaction with previously obtained data
def date_compare(date1, date2):
    year1,month1,day1 = date1.split('-')
    year2,month2,day2 = date2.split('-')

    if year2 > year1:
        return date2
    elif year1 > year2:
        return date1
    elif month2 > month1:
        return date2
    elif month1 > month2:
        return date1
    elif day2 > day1:
        return date2
    elif day1 > day2:
        return date1
    else:
        return None
        
def test_latest_date():
	last_trans = latest_transactions()
	latest_date = ''
	for item in last_trans['last_10_transactions']:
		if latest_date=='':
			latest_date = item['date']
		else:
			new_date = date_compare(latest_date, item['date'])
			if new_date !=None:
		    		latest_date = new_date
	print(latest_date)
	assert latest_date == '2021-04-16'

