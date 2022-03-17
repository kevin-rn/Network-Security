import sys
import smtplib
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

    try:
        # server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server = smtplib.SMTP("smtp.gmail.com", 587)
        # server.set_debuglevel(1)
        server.ehlo()
        server.starttls()
        server.login(sender_mail, sender_password)
        server.send_message(msg)
        server.close()
        print(mail_text)
    except:
        pass 
