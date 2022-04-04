import requests
import time
from threading import Thread

# host = 'localhost'
host = '192.168.200.104'
wp_login = f'http://{host}/wordpress/wp-login.php'
wp_admin = f'http://{host}/wordpress/wp-admin/'
username = 'wordpress'
valid_password = 'Wordpress123'
bad_password = 'garbage'

def make_full_request(password):
    with requests.Session() as s:
        headers1 = { 'Cookie':'wordpress_test_cookie=WP Cookie check' }
        datas={ 
            'log':username, 'pwd':password, 'wp-submit':'Log In', 
            'redirect_to':wp_admin, 'testcookie':'1'  
        }
        s.post(wp_login, headers=headers1, data=datas, allow_redirects=False)
        resp = s.get(wp_admin)
        return resp.url == wp_admin

headers1 = { 'Cookie':'wordpress_test_cookie=WP Cookie check' }
datas={ 
    'log':username, 'pwd':bad_password, 'wp-submit':'Log In', 
    'redirect_to':wp_admin, 'testcookie':'1'  
}

def make_request():
    with requests.Session() as s:
        try:
            resp = s.post(wp_login, headers=headers1, data=datas, timeout=1)
            print(time.time_ns())
            return True
        except:
            return False

# print(make_full_request(valid_password))
# make_full_request(bad_password)
# print(make_request())

for i in range(20):
    Thread(target=make_request).start()

time.sleep(4)