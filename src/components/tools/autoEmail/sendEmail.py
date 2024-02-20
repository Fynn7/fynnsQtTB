import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import schedule
import time
import re


def is_valid_email(email: str) -> bool:
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def schedule_email(sender_email:str, sender_password:str, recipient_email:str, subject:str="Daily Report", body:str="Hello,\n\nThis is your daily report.",schedule_time:str="08:00",pending_interval:int=1):
    def send_email():
        message = MIMEMultipart()
        if not is_valid_email(sender_email) or not is_valid_email(recipient_email):
            raise ValueError("Invalid email address.")
        message["From"] = sender_email
        message["To"] = recipient_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        # Connect to the SMTP server (Gmail example)
        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, message.as_string())

        print("Email sent successfully.")

    # Schedule the script to run daily at a specific time (adjust as needed)
    schedule.every().day.at(schedule_time).do(send_email)

    while True:
        schedule.run_pending()
        time.sleep(pending_interval)
