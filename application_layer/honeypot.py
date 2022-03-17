import sys
from socket import socket, AF_INET, SOCK_STREAM
from datetime import datetime

# Helper method for logging data to logFile
def logData(address, message, data):
    now = datetime.now()
    str_format = "Time: {}\nIP: {}\nPort: {}\nMessage: {}\nData: {}\n".format(now, address[0], address[1], message, data)
    with open('logFile', 'a+') as f:
        f.write(str_format)
        f.close()

if __name__ == "__main__":
    ip = str(sys.argv[1])
    port = int(sys.argv[2])
    message = str(sys.argv[3])

    # Create socket and listen to provided ip address and port.
    sock = socket(AF_INET,SOCK_STREAM)
    sock.bind((ip, port))
    sock.listen()

    # For each connection client log the information.
    while True:
        try:
            connection, address = sock.accept()
            connection.sendall(message.encode()) # send message to client
            data = connection.recv(2048)
            data = data.decode()
            connection.close()                   # close current connection
            logData(address, message, data)      # log data

        except (KeyboardInterrupt, Exception):
            sock.close()
            quit()