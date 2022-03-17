import sys
from socket import socket, AF_INET, SOCK_STREAM

if __name__ == "__main__":
    ip = str(sys.argv[1])
    port = str(sys.argv[2])
    message = str(sys.argv[3])

    sock = socket(AF_INET,SOCK_STREAM)
    sock.bind((ip, port))
    sock.listen()
    connection, address = sock.accept()