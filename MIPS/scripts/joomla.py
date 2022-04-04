# from scapy.all import *
import re
import requests
# import json

# data = {
#     "username": "root",
#     "passwd": "root",
#     "option": "com_login",
#     "task": "login",
#     "return": "aW5kZXgucGhw",
#     "ec1517a8f7513f09833836e09e15bad1": "1"
# }

target = 'http://localhost/joomla/administrator/index.php'

session = requests.Session()

response = session.get(target)

hidden_tags = re.findall(r'<input.+type="hidden".+>', response.text)
print(hidden_tags)
print(hidden_tags[3])

# Get the randomized token - which is the 6th hidden field in the form
token_name = re.findall(r'name="(\S+)"', hidden_tags[3])[0]
token_val = re.findall(r'value="(\S+)"', hidden_tags[3])[0]

login_data = {
    "username": 'root',
    "password": 'root',
    "remember": "yes",
    "return": "",
    token_name: token_val,
}

login_response = session.post(target, data=login_data, allow_redirects=False)

login_cookie = login_response.headers.get('set-cookie', "")

print("joomla_user_state=logged_in" in login_cookie)
