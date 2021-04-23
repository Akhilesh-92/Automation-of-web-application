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


#  Get the savings account details using api
def account_info():
	account_res = requests.get(url='http://demo.testfire.net/api/account', headers=headers)
	account_info = json.loads(account_res.content)
	return account_info
	
def test_account_info():
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


# Find all transactions for the current month using api
def all_transactions():
	acc_info = account_info()
	url1 = 'https://demo.testfire.net/api/account' + '/' + acc_info['Accounts'][0]['id'] + '/' + 'transactions'
	payload1 = {
	    "startDate": "2021-04-16",
	    "endDate": "2021-04-16"
	}
	res1 = requests.post(url=url1, headers=headers, json=payload1, verify=False)
	data1 = json.loads(res1.content)
	return data1
	
def test_all_trans():
	all_trans = all_transactions()
	assert all_trans['transactions'][0]['account'] == '800002'


#  Filter only credited transactions
def test_total_credits():
	all_trans = all_transactions()
	credit_sum = 0
	for ele in all_trans['transactions']:
		if ele['type'] == 'Deposit':
			 credit_sum = credit_sum + float(ele['amount'].replace('$',''))
	print(credit_sum)
	assert credit_sum != None 


# Calculate the sum of all credited transactions
# credit_sum = 0
# for item in credited_trans:
#     credit_sum = credit_sum + float(item['ammount'].replace('$',''))
# print(credit_sum)

# # use smtp python library and send an email to your personal gmail id
# import smtplib
# Email_Address = 'akhilesh.rymec@gmail.com'
# password = 'xspalimruexjugcg'
# with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
# 	smtp.ehlo()
# 	smtp.starttls()
# 	smtp.ehlo()
# 	smtp.login(Email_Address, password)
# 	subject = "Bank Account transaction"
# 	body = 'Savings account id - {0}\nSum of all credits - {1}\nCurrent Month - {2}'.format(acc_id,credit_sum,'March')
# 	msg = f'Subject: {subject}\n\n{body}'
# 	smtp.sendmail(Email_Address, 'akhilesh29392@gmail.com', msg)
