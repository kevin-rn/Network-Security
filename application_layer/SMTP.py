import sys
import ssl
from os.path import basename
from socket import socket, AF_INET, SOCK_STREAM
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def createMessage(sender: str, receiver: str, attachment: str, body: str):
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = receiver
    message['Subject'] = 'New Email'
    message.attach(MIMEText(body, 'plain'))

    with open(attachment, "rb") as attachment_fil:
        filename = basename(attachment)                                             # extracts filename from the provided path
        attachment_file = MIMEApplication(attachment_fil.read(), Name=filename)

    attachment_file['Content-Disposition'] = 'attachment; filename="%s"' % filename
    message.attach(attachment_file)
    return message.as_string() + "\r\n.\r\n"

def format_send(input_str: str):
    result = input_str.encode() + "\r\n".encode()
    return result

def sendMail(sender: str, password: str, receiver: str, message: str):
    clientSocket = socket(AF_INET, SOCK_STREAM)
    
    clientSocket.connect(('smtp.gmail.com', 587))
    response = clientSocket.recv(1024)
    response = response.decode()
    print(response)

    ehlo = "ehlo localdomain" # {}\r\n".format(socket.getfqdn())
    clientSocket.send(format_send(ehlo))
    response = clientSocket.recv(1024)
    response = response.decode()
    print(response)
    
    clientSocket.send(format_send("STARTTLS"))
    response = clientSocket.recv(1024)
    response = response.decode()
    print(response)
    
    context = ssl.create_default_context()
    clientSocketTLS = context.wrap_socket(clientSocket, server_hostname='smtp.gmail.com')
    # clientSocketTLS = ssl.wrap_socket(clientSocket, ssl_version=ssl.PROTOCOL_TLS)
    clientSocketTLS.send(format_send("AUTH LOGIN"))
    response = clientSocketTLS.recv(1024)
    response = response.decode()
    print(response)
    
    clientSocketTLS.send(base64.b64encode(sender.encode()) + "\r\n".encode() )
    response = clientSocketTLS.recv(1024)
    response = response.decode()
    print(response)
    
    clientSocketTLS.send(base64.b64encode(password.encode()) + "\r\n".encode())
    response = clientSocketTLS.recv(1024)
    response = response.decode()
    print(response)

    clientSocketTLS.send(format_send("MAIL FROM:<" + sender + ">"))
    response = clientSocketTLS.recv(1024)
    response = response.decode()
    print(response)

    clientSocketTLS.send(format_send("RCPT TO:<" + receiver + ">"))
    response = clientSocketTLS.recv(1024)
    response = response.decode()
    print(response)

    clientSocketTLS.send(format_send("DATA"))
    response = clientSocketTLS.recv(1024)
    response = response.decode()
    print(response)

    clientSocketTLS.send(format_send(message))
    response = clientSocketTLS.recv(1024)
    response = response.decode()
    print(response)
    
    clientSocketTLS.send(format_send("QUIT"))
    response = clientSocketTLS.recv(1024)
    response = response.decode()
    print(response)
    
    clientSocketTLS.close()
    clientSocket.close()

if __name__ == "__main__":
    sender_mail = str(sys.argv[1])
    sender_password = str(sys.argv[2])
    receiver_mail = str(sys.argv[3])
    attachment = str(sys.argv[4])
    body = str(sys.argv[5])

    mail_text = "From: {}\r\nTo: {}\r\nSubject: New Email\r\nBody: {}\nAttachment: {}".format(sender_mail, receiver_mail, body, attachment)
    message = createMessage(sender=sender_mail, receiver=receiver_mail, attachment=attachment, body=body)

    sendMail(sender=sender_mail, password=sender_password, receiver=receiver_mail, message=message)
    print(mail_text)
