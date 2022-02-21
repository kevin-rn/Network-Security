# Network-Security

```python
import re 
from subprocess import Popen, PIPE, DEVNULL
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

DIR = "/var/log/"
FNAME = "auth.log"

class FileModifiedHandler(FileSystemEventHandler):

    def __init__(self, loghandle):
        self.loghandle = loghandle

        # set observer to watch for changes in the directory
        self.observer = Observer()
        self.observer.schedule(self, DIR, recursive=False)
        self.observer.start()
        self.observer.join()

    # Check if /var/log/auth.log changed
    def on_modified(self, event): 
        if not event.is_directory and event.src_path.endswith(FNAME):
            self.observer.stop() # stop watching
            self.loghandle() # call callback

def print_log(authlog):
    if "phpMyAdmin" in authlog:
        split_str = re.split(' ', authlog)
        # timestamp = str.join(map(split_str.__getitem__, [0, 1, 2]))
        timestamp = " ".join(split_str[0:3])
        username = split_str[7]
        ip = split_str[10]
        print("Timestamp: {}, username: {}, ip address: {}".format(timestamp, username, ip))
    else:
        print("No failed authentication found.")

if __name__ == '__main__':
    # authlog = "Feb 20 23:21:13 virtual phpMyAdmin[2607]: user denied: admin (mysql-denied) from 127.0.0.1"
    
    def loghandle():
        process = Popen(['tail','-1',DIR+FNAME],shell=False, stderr=DEVNULL, stdout=PIPE)
        res, _ = process.communicate()
        authlog = str(res.decode())
        print_log(authlog)
        
    FileModifiedHandler(loghandle)  



```
