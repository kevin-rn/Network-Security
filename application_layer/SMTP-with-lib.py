import sys
import smtplib
from email.message import EmailMessage

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

if __name__ == "__main__":
    sender_mail = str(sys.argv[1])
    sender_password = str(sys.argv[2])
    receiver_mail = str(sys.argv[3])
    attachment = str(sys.argv[4])
    body = str(sys.argv[5])

    # msg = EmailMessage()
    # msg['From'] = sender_mail
    # msg['To'] = receiver_mail
    # msg['Subject'] = "New Email"
    # msg.set_content(body)
    # msg.add_attachment(attachment)

    sender_address = sender_mail
    sender_pass = sender_password
    receiver_address = receiver_mail
    mail_content = body

    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'New Email'

    message.attach(MIMEText(mail_content, 'plain'))
    attach_file_name = attachment
    attach_file = open(attach_file_name, 'rb')  # Open the file as binary mode
    payload = MIMEBase('application', 'octet-stream')
    payload.set_payload((attach_file).read())
    encoders.encode_base64(payload)  # encode the attachment
    attach_file.close()
    payload.add_header('Content-Disposition', 'attachment', filename=attach_file_name)
    message.attach(payload)

    # mail_text = "From: {}\nTo: {}\nSubject: New Email\nBody: {}\nAttachment: {}".format(sender_mail, receiver_mail, body, attachment)

    try:
        # server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server = smtplib.SMTP("smtp.gmail.com", 587)
        # server.set_debuglevel(1)
        server.ehlo()
        server.starttls()
        server.login(sender_mail, sender_password)
        server.sendmail(sender_mail, receiver_mail, message.as_string())
        server.close()
        print(message.as_string())
    except:
        pass 
