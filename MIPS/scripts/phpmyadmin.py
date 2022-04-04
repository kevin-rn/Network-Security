# https://c0deman.wordpress.com/2014/06/04/phpmyadmin-automation-python-script/
import requests
from threading import Thread
import time
 
host = '192.168.200.104'
url = f'http://{host}/phpmyadmin/index.php'
user = "root"
password = "roota"

check = True

def make_request():
    with requests.Session() as s:
        try:
            response = s.get(url,timeout=1)
            token = response.content.split(b'name="token"')[1].split(b'"')[1]

            loginpayload = {
                "set_session": "4ugr0fkma23uaumdpkv8i9msdk",
                "pma_username": user,
                "pma_password": password,
                "server": "1",
                "target": "index.php",
                "token": token
            }
             
            response = s.post(url,data=loginpayload, timeout=1)
            print(time.time_ns())
            return True
        except:
            # if check:
            #     check = False
            print("False: " + str(time.time_ns()))
            return False


for i in range(50):
    Thread(target=make_request).start()

time.sleep(4)
                 