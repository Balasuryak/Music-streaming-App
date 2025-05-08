from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SMTP_SERVER="localhost"
SMTP_PORT=1025
SENDER_EMAIL='BS@email.com'
SENDER_PASSWORD='abcdef'


def send_message(to, subject, content_body):
    msg = MIMEMultipart()
    msg["To"] = to
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg.attach(MIMEText(content_body, 'html'))
    client = SMTP(host=SMTP_SERVER, port=SMTP_PORT)
    client.send_message(msg=msg)
    client.quit()