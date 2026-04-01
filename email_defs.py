import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from itsdangerous import URLSafeTimedSerializer
from flask import url_for
from CRUDEMANAGER.crud.read import UserRead
from CRUDEMANAGER.maindefs import connect
from CRUDEMANAGER.crud.update import UserEdit

EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASS = os.getenv('EMAIL_PASS')
SMTP_HOST = os.getenv('SMTP_HOST')
SMTP_PORT = int(os.getenv('SMTP_PORT', 465))

serializer = URLSafeTimedSerializer(os.getenv('FLASK_SECRET_KEY'))

def send_reset_email(email, reset_url):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = email
    msg['Subject'] = 'Password Reset Request'

    body = f'Please click the link to reset your password: {reset_url}'
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT)
        server.login(EMAIL_USER, EMAIL_PASS)
        text = msg.as_string()
        server.sendmail(EMAIL_USER, email, text)
        server.quit()
        print(f"Email sent successfully to {email}")
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def generate_reset_token(email):
    return serializer.dumps(email, salt='password-reset-salt')

def verify_reset_token(token, max_age=3600):
    try:
        email = serializer.loads(token, salt='password-reset-salt', max_age=max_age)
        return email
    except:
        return None

def send_password_reset_email(email, app):
    token = generate_reset_token(email)
    reset_url = url_for('reset_password', token=token, _external=True)
    return send_reset_email(email, reset_url)

def update_password(email, new_password, table='databasedusers'):
    connection = connect()
    if not connection:
        return False
    try:
        user_id = UserRead(email, table).read_id(connection)
        UserEdit(user_id, "password", new_password, table).update(connection)
        print(f"Password updated successfully for {email}")
        return True
    except Exception as e:
        print(f"Error updating password: {e}")
        return False
    finally:
        connection.close()

def generate_verification_token(email):
    return serializer.dumps(email, salt='email-confirm-salt')

def verify_confirmation_token(token, max_age=86400):
    try:
        email = serializer.loads(token, salt='email-confirm-salt', max_age=max_age)
        return email
    except:
        return None

def send_verification_email(email, name):
    token = generate_verification_token(email)
    confirm_url = url_for('confirm_email', token=token, _external=True)
    
    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = email
    msg['Subject'] = 'Confirm Your Email Address'

    body = f"""
    Hello, {name}!

    Thank you for registering. To activate your account, please click the link below:
    {confirm_url}

    This link will expire in 24 hours.
    """
    
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT)
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(EMAIL_USER, email, msg.as_string())
        server.quit()
        print(f"Verification email sent to {email}")
        return True
    except Exception as e:
        print(f"Error sending verification email: {e}")
        return False