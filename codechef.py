# from flask import Flask
# app = Flask(__name__)

# @app.route('/')
# def hello_world():
#     return 'Hello, World!'

#!/usr/bin/env python
from flask import Flask, abort, request
from uuid import uuid4
import requests
import requests.auth
import urllib
import json
import os
CLIENT_ID = "79bad34730516fb7f3971626c64bd371"
CLIENT_SECRET = "09ced10b8039541daf84a639c2dd5ca4" 
REDIRECT_URI = "http://localhost:5000/reddit_callback"


########################################### OLD ##########################################

# import urllib.request,urllib.parse,json,sys
# url = "https://api.codechef.com/contests/"+urllib.parse.urlencode({'contestCode':PRACTICE})+"/problems/"+urllib.parse.urlencode({'problemCode':SALARY})+"?fields="
# # data = "SALARY"
# # header = {'Authorization': b'Basic' + b64encode(('cloud-api').encode('utf-8'))}
# # data = urlencode(dict(username='USERNAME',password='PASSWORD')).encode('ascii')

# res=urllib.request.urlopen(url)
# json_data=json.load(res)
# # url = 'https://referencedatacloudauth.sit.icg.citigroup.net/auth/token?grant_type=velocity_169234/securities/products?search={"Xref.CSP":"G6264VAA0"}'
# print (res)
# print (json)

# import requests
# from pprint import pprint

# Client ID="690dc30971b0cb08250c252739dc9197"
# Client Secret="b14a6d92b469ca9d475cdfa6aacb5963"

# params = (
#     ('fields', ''),
# )

# response = requests.get('https://api.codechef.com/contests/%7BcontestCode%7D/problems/%7BproblemCode%7D', params=params)

############################## CORRECT ##################################################
# contestCode="PRACTICE"
# problemCode="SALARY"
# response = requests.get('https://api.codechef.com/contests/{contestCode}/problems/{problemCode}?fields=')
# print (response)



# headers = {
#     'content-Type': 'application/json',
# }

# data = '{"grant_type": "authorization_code","code": "561b5d25f7f0062e7102d17da5c535fb6d3dbfb2","client_id":"79bad34730516fb7f3971626c64bd371","client_secret":"09ced10b8039541daf84a639c2dd5ca4","redirect_uri":"https://www.google.com"}'

# response = requests.post('http://api.codechef.com/oauth/token', headers=headers, data=data)
# # response = requests.get("https://api.codechef.com/oauth/authorize?response_type=code&client_id=79bad34730516fb7f3971626c64bd371&state=raghav&redirect_uri=https://www.google.com")
# print (response)
# https://www.google.com/?code=40428059cf90c0c49b60ebfbbb9678b65e231485&state=raghav
#############3LOCAL HOST#################################
# import requests

# headers = {
#     'content-Type': 'application/json',
# }

# data = '{"grant_type": "authorization_code","code": "260286e8cb66967900473c452fd4cbc6be1d41f4","client_id":"79bad34730516fb7f3971626c64bd371","client_secret":"09ced10b8039541daf84a639c2dd5ca4","redirect_uri":"https://www.google.com"}'

# response = requests.post('http://api.codechef.com/oauth/token', headers=headers, data=data)
# print (response)

# data = [
#   ('grant_type', 'client_credentials'),
#   ('client_id', '79bad34730516fb7f3971626c64bd371'),
#   ('client_secret', '09ced10b8039541daf84a639c2dd5ca4'),
#   ('scope', 'public'),
#   ('redirect_uri', 'https://www.google.com'),
# ]

# response = requests.post('http://api.codechef.com/oauth/token', headers=headers, data=data)
# print (response)

# http://api.codechef.com/oauth/token/grant_type=client_credentials&client_id=690dc30971b0cb08250c252739dc9197&client_secret=b14a6d92b469ca9d475cdfa6aacb5963&scope=public&redirect_uri=https://www.google.com



############################################# NEW ###########################################################



app = Flask(__name__)
@app.route('/')
def homepage():
    text = '<a href="%s">Authenticate with CodeChef</a>'
    return text % make_authorization_url()


# def make_authorization_url():
#     state="raghav"
#     save_created_state(state)
#     params = {"response_type": "code","client_id": CLIENT_ID,"redirect_uri": REDIRECT_URI,"state":state
#               }
#     url = "https://api.codechef.com/oauth/authorize?" + urllib.urlencode(params)
#     return url

# def save_created_state(state):
#     pass
# def is_valid_state(state):
#     return True

# @app.route('/reddit_callback')
# def reddit_callback():
#     error = request.args.get('error', '')
#     if error:
#         return "Error: " + error
#     state = request.args.get('state', '')
#     if not is_valid_state(state):
#         abort(403)
#     code = request.args.get('code')
#     # print (code)

#     text = '<a href="%s">Click For Access Token</a>'
#     return text % get_token(code)

# def get_token(code):
    
#     post_data = '{"grant_type": "authorization_code","code": "code","client_id":"d2d1029a2eb5f59b97536f683e3f1a88","client_secret":"c346b3139d6afc6ce5226a0df04ca2a9","redirect_uri":"http://localhost:5000/reddit_callback"}'

#     headers = {
#     'content-Type': 'application/json',
# 	}
#     response = requests.post("https://api.codechef.com/oauth/token",
#                              headers=headers,
#                              data=post_data)
#     print (response)
#     return response

# def get_token(code):
# 	# print (code)
# 	new_code=str(code)
# 	# d3 = json.dumps(json.loads(code)) 
#     # client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET) 
# 	post_data = {"grant_type": "authorization_code","code":new_code,"client_id":"79bad34730516fb7f3971626c64bd371","client_secret":"09ced10b8039541daf84a639c2dd5ca4","redirect_uri":"http://localhost:5000/reddit_callback"}
# 	# print post_data
# 	r = json.dumps(post_data) # converting dict to string(json)
# 	print (r)
# 	headers = {'content-Type': 'application/json'}
# 	response = requests.post("https://api.codechef.com/oauth/token",headers=headers,data=r)
# 	print (response.content)
# 	print (response)
# 	return (response)                                       
# def get_username(access_token):
#     headers = base_headers()
#     headers.update({"Authorization": "bearer " + access_token})
#     response = requests.get("https://oauth.reddit.com/api/v1/me", headers=headers)
#     me_json = response.json()
#     return me_json['name']


if __name__ == '__main__':
    app.run(debug=True, port=5000)

###################################### TRY ######################################################
# req = requests.Request('POST','http://stackoverflow.com',headers={'X-Custom':'Test'},data='a=1&b=2')
# curl -X POST https://api.codechef.com/oauth/token -H 'content-Type: application/json' -d '{"grant_type": "authorization_code","code": "your_authorization_code","client_id":"your_client_id","client_secret":"your_client_secret","redirect_uri":"your_redirect_uri"}'



# curl -X POST https://api.codechef.com/oauth/token -H 'content-Type: application/json' -d '{"code": "e7c3a0968a8c37cef0c30da9b2d15888190c22b4", "client_secret": "09ced10b8039541daf84a639c2dd5ca4", "grant_type": "authorization_code", "client_id": "79bad34730516fb7f3971626c64bd371", "redirect_uri": "http://localhost:5000/reddit_callback"}'
# '{'grant_type': 'authorization_code','code': u'e9f22eb798f2cbd813f2909efa037d021eefb3c5','client_id': '79bad34730516fb7f3971626c64bd371','client_secret': '09ced10b8039541daf84a639c2dd5ca4','redirect_uri': 'http://localhost:5000/reddit_callback'}'
# '{'code': u'362f285397c6d88e44e7cf58de4b63b267c4c4fe', 'client_secret': '09ced10b8039541daf84a639c2dd5ca4', 'grant_type': 'authorization_code', 'client_id': '79bad34730516fb7f3971626c64bd371', 'redirect_uri': 'http://localhost:5000/reddit_callback'}'


# '{"code": "e7c3a0968a8c37cef0c30da9b2d15888190c22b4", "client_secret": "09ced10b8039541daf84a639c2dd5ca4", "grant_type": "authorization_code", "client_id": "79bad34730516fb7f3971626c64bd371", "redirect_uri": "http://localhost:5000/reddit_callback"}'

##################################################### TOKEN USE ###########################################