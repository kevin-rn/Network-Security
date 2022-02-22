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
