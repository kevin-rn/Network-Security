# Network-Security

```python
import re, time 
from subprocess import Popen, PIPE, DEVNULL
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

DIR = "/var/log/"
FNAME = "auth.log"

# Watcher class for observing changes of file in directory
class Watcher:
    def __init__(self):
        self.observer = Observer()

    # Through unix command retrieve last line of the file and call print_log on it.
    def loghandle(self):
        process = Popen(['tail','-1',DIR+FNAME],shell=False, stderr=DEVNULL, stdout=PIPE)
        res, _ = process.communicate()
        authlog = str(res.decode())
        print_log(authlog)

    # Runs the observer continuously until keyboardinterrupt occurs (cntrl C).
    def run(self):
        event_handler =  FileModifiedHandler(self.loghandle) 
        self.observer.schedule(event_handler, DIR, recursive=False)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
            print("Stopped")
        self.observer.join()

# Handler class that detects the type of change that occurs.
class FileModifiedHandler(FileSystemEventHandler):
    def __init__(self, loghandle):
        self.loghandle = loghandle

    # Check if /var/log/auth.log changed
    def on_modified(self, event): 
        if not event.is_directory and event.src_path.endswith(FNAME):
            self.loghandle() # call callback

# Helper method for processing the results.
def print_log(authlog):
    #E.g. "Feb 20 23:21:13 virtual phpMyAdmin[2607]: user denied: admin (mysql-denied) from 127.0.0.1"
    if "phpMyAdmin" in authlog:
        split_str = re.split(' ', authlog)
        timestamp = " ".join(split_str[0:3])
        username = split_str[7]
        ip = split_str[10]
        print("Timestamp: {}, username: {}, ip address: {}".format(timestamp, username, ip))
    else:
        print("No failed authentication found.")

# main method
if __name__ == '__main__':
    w = Watcher()
    w.run()
```

```python
import re, time 
from subprocess import Popen, PIPE, DEVNULL
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

DIR = "/var/www/html/joomla/administrator/logs/"
FNAME = "error.php"

# Watcher class for observing changes of file in directory
class Watcher:
    def __init__(self):
        self.observer = Observer()

    # Through unix command retrieve last line of the file and call print_log on it.
    def loghandle(self):
        process = Popen(['tail','-1',DIR+FNAME],shell=False, stderr=DEVNULL, stdout=PIPE)
        res, _ = process.communicate()
        authlog = str(res.decode())
        print_log(authlog)

    # Runs the observer continuously until keyboardinterrupt occurs (cntrl C).
    def run(self):
        event_handler =  FileModifiedHandler(self.loghandle) 
        self.observer.schedule(event_handler, DIR, recursive=False)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
            print("Stopped")
        self.observer.join()

# Handler class that detects the type of change that occurs.
class FileModifiedHandler(FileSystemEventHandler):
    def __init__(self, loghandle):
        self.loghandle = loghandle

    # Check if /var/log/auth.log changed
    def on_modified(self, event): 
        if not event.is_directory and event.src_path.endswith(FNAME):
            self.loghandle() # call callback

# Helper method for processing the results.
def print_log(authlog):
    #E.g. 2018-05-25T22:10:26+00:00       INFO 127.0.0.1      joomlafailure   Username and password do not match or you do not have an account yet.
    if "joomlafailure" in authlog:
        split_str = authlog.split()
        timestamp = split_str[0] # 2022-02-27T23:24:18+00:00
        ip_address = split_str[2] # 127.0.0.1
        print("Timestamp: {}, ip address: {}".format(timestamp, ip_address))
    else:
        print("No failed authentication found.")

# main method
if __name__ == '__main__':
    w = Watcher()
    w.run()
```

import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("ERROR")
        exit()

    input_str = str(sys.argv[1])
    if len(input_str) > 50:
        print("ERROR")
        exit()

    one_time_chars = ['B', 'H', 'Z', 'A', 'P', 'S', 'I', 'E', 'Z', 'S', 
    'L', 'A', 'G', 'V', 'C', 'E', 'X', 'L', 'E', 'U', 'F', 'X', 'X', 'X', 
    'G', 'O', 'F', 'J', 'L', 'D', 'H', 'S', 'O', 'S', 'C', 'O', 'Q', 'O', 
    'J', 'G', 'X', 'W', 'W', 'P', 'R', 'Z', 'X', 'D', 'M', 'M']

    bytes_str = input_str.encode()
    otp = ""
    for index, byte_txt in enumerate(bytes_str):
        byte_key = ord(one_time_chars[index])
        mod_add = (byte_key + ord(byte_txt)) % 2
        otp += str(mod_add)
    print(otp)


from email.policy import default
from nis import match

from cupshelpers import Printer
import numpy as np
from scipy.optimize import curve_fit
import sys

def computeNumberOfStrings(n, lngth)


def fitCurve(x, y):
    def func(x, c, d):
        return c * np.exp(d * x)

    params, _ = curve_fit(func, x, y, p0=(1., 1.))

    return params.tolist()

def exactParams(n):
    # compute/return the exact params c and d

    return [c, d]


if __name__ == "__main__":
    if len(sys.argv) != 3 or len(sys.argv) != 4:
        print("ERROR")

    func_name = str(sys.argv[1])
    arg1 = sys.argv[2]
    arg2 = sys.argv[3]

    ## Match only available in python 3.10+
    # match func_name:
    #     case 'computeNumberOfStrings': 
    #         computeNumberOfStrings(arg1, arg2)
    #     case 'fitCurve': 
    #         fitCurve(arg1, arg2)
    #     case 'exactParams': 
    #         exactParams(arg1)
    #     default:
    #         print("ERROR")

    if func_name == 'computeNumberOfStrings':
        computeNumberOfStrings(arg1, arg2)
    elif func_name == 'fitCurve':
        fitCurve(arg1, arg2)
    elif func_name == 'exactParams':
        exactParams(arg1)
    else:
        print("ERROR")
