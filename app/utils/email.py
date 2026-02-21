import os
import smtplib

from email.message import EmailMessage


def send_email(to_email: str, subject: str, body: str):
    email_user = os.getenv("EMAIL_USER")
    email_password = os.getenv("EMAIL_PASSWORD")

    msg = EmailMessage()
    msg["From"] = email_user
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP("smtp.mail.ru", 587) as server:
        server.starttls()
        server.login(email_user, email_password)
        server.send_message(msg)
