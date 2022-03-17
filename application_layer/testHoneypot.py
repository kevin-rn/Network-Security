from socket import *

# Use to test if honeypot script works by connecting to the same port and send message
if __name__ == "__main__":
    sock = socket(AF_INET,SOCK_STREAM)
    sock.connect(("127.0.0.1", 9999))
    message = "This is a test sentence to send"
    sock.sendall((message.encode()))
    sock.close()