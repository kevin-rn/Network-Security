import sys
from socket import socket, AF_INET, SOCK_STREAM
import ssl
import base64
from email.message import EmailMessage

if __name__ == "__main__":
    sender_mail = str(sys.argv[1])
    sender_password = str(sys.argv[2])
    receiver_mail = str(sys.argv[3])
    attachment = str(sys.argv[4])
    body = str(sys.argv[5])

    msg = EmailMessage()
    msg['From'] = sender_mail
    msg['To'] = receiver_mail
    msg['Subject'] = "New Email"
    msg.set_content(body)
    msg.add_attachment(attachment)

    mail_text = "From: {}\nTo: {}\nSubject: New Email\nBody: {}\nAttachment: {}".format(sender_mail, receiver_mail, body, attachment)

    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect(('smtp.gmail.com', 587))
    recv = clientSocket.recv(1024)
    recv = recv.decode()
    if recv[:3] != '220':
        print('220 reply not received from server: ', recv)
        quit()

    clientSocket.send("EHLO Alice\r\n".encode())
    recv = clientSocket.recv(1024)
    recv = recv.decode()
    if recv[:3] != '250':
        print('250 reply on EHLO not received from server: ', recv)
        quit()

    clientSocket.send("STARTTLS\r\n".encode())
    recv = clientSocket.recv(1024)
    recv = recv.decode()
    if recv[:3] != '220':
        print('250 reply on STARTTLS not received from server: ', recv)
        quit()

    clientSocket.send("AUTH PLAIN\r\n".encode())
    recv = clientSocket.recv(1024)
    recv = recv.decode()
    if recv[:3] != '250':
        print('250 reply on AUTH PLAIN not received from server: ', recv)
        quit()

    authentication = base64.b64encode((sender_mail+"\0"+sender_password).encode())
    clientSocket.send(authentication)
    recv = clientSocket.recv(1024)
    if recv[:3] != '250':
        print('250 reply on authentication not received from server: ', recv)
        quit()

    clientSocket.send(msg.as_bytes())
    recv = clientSocket.recv(1024)
    if recv[:3] != '250':
        print('250 reply on message not received from server: ', recv)
        quit()

    clientSocket.send("QUIT\r\n".encode())
    recv = clientSocket.recv(1024)
    if recv[:3] != '250':
        print('250 reply on Quit not received from server: ', recv)
        quit()
    clientSocket.close()

    print(mail_text)