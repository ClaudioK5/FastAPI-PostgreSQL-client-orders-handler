import sys
import smtplib
from email.message import EmailMessage

def send_email(to_email, subject, body):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = 'insert your bot email here'
    msg['To'] = to_email
    msg.set_content(body)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('insert your bot email here','insert your bot password here')
        smtp.send_message(msg)
