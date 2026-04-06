import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from flask import url_for

from CRUDEMANAGER.crud.read import UserRead
from CRUDEMANAGER.crud.update import UserEdit
from CRUDEMANAGER.maindefs import connect

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 465))

PASSWORD_RESET_SALT = "password-reset-salt"
EMAIL_CONFIRM_SALT = "email-confirm-salt"

serializer = URLSafeTimedSerializer(os.getenv("FLASK_SECRET_KEY", ""))


def _send_email(receiver, subject, body):
    if not (EMAIL_USER and EMAIL_PASS and SMTP_HOST):
        print("Error sending email: SMTP configuration is incomplete.")
        return False

    msg = MIMEMultipart()
    msg["From"] = EMAIL_USER
    msg["To"] = receiver
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
            server.login(EMAIL_USER, EMAIL_PASS)
            server.sendmail(EMAIL_USER, receiver, msg.as_string())

        print(f"Email sent successfully to {receiver}")
        return True
    except Exception as error:
        print(f"Error sending email: {error}")
        return False


def send_reset_email(email, reset_url):
    subject = "Password Reset Request"
    body = f"Please click the link to reset your password: {reset_url}"
    return _send_email(email, subject, body)


def generate_reset_token(email):
    return serializer.dumps(email, salt=PASSWORD_RESET_SALT)


def verify_reset_token(token, max_age=3600):
    try:
        return serializer.loads(token, salt=PASSWORD_RESET_SALT, max_age=max_age)
    except (BadSignature, SignatureExpired):
        return None


def send_password_reset_email(email):
    token = generate_reset_token(email)
    reset_url = url_for("reset_password", token=token, _external=True)
    return send_reset_email(email, reset_url)


def update_password(email, new_password, table="databasedusers"):
    connection = connect()
    if not connection:
        return False

    try:
        user_id = UserRead(email, table).read_id(connection)
        if not user_id:
            print(f"Error updating password: user not found ({email})")
            return False

        UserEdit(user_id, "password", new_password, table).update(connection)
        print(f"Password updated successfully for {email}")
        return True
    except Exception as error:
        print(f"Error updating password: {error}")
        return False
    finally:
        connection.close()


def generate_verification_token(email):
    return serializer.dumps(email, salt=EMAIL_CONFIRM_SALT)


def verify_confirmation_token(token, max_age=86400):
    try:
        return serializer.loads(token, salt=EMAIL_CONFIRM_SALT, max_age=max_age)
    except (BadSignature, SignatureExpired):
        return None


def send_verification_email(email, name):
    token = generate_verification_token(email)
    confirm_url = url_for("confirm_email", token=token, _external=True)

    body = f"""
    Hello, {name}!

    Thank you for registering. To activate your account, please click the link below:
    {confirm_url}

    This link will expire in 24 hours.
    """

    return _send_email(email, "Confirm Your Email Address", body)
