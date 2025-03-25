import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SERVER_SMTP_HOST = 'localhost'
SERVER_SMTP_PORT = 1025
SENDER_ADDRESS = "app.dev.yash@gmail.com"
SENDER_PASSWORD = ''

def send_mail(receiver="yashsrivastava02112000@gmail.com", message="", subject= "From BlogSite"):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = SENDER_ADDRESS
    msg['To'] = receiver
    msg.attach(MIMEText(message, 'html'))
    
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
        gmail_password= "hxqj uvxp nkzy avwc "
        s.login("app.dev.yash@gmail.com", gmail_password)
        s.send_message(msg)
        s.quit()
        print("EMAIL SENT")
