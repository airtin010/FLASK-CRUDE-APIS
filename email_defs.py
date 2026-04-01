import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from itsdangerous import URLSafeTimedSerializer
from flask import url_for
from CRUDEMANAGER.crud.read import readuser
from CRUDEMANAGER.maindefs import conectar
from CRUDEMANAGER.crud.update import edituser

EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASS = os.getenv('EMAIL_PASS')
SMTP_HOST = os.getenv('SMTP_HOST')
SMTP_PORT = int(os.getenv('SMTP_PORT', 465))

serializer = URLSafeTimedSerializer(os.getenv('FLASK_SECRET_KEY'))

def send_reset_email(email, reset_url):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = email
    msg['Subject'] = 'Redefinição de Senha'

    body = f'Clique no link para redefinir sua senha: {reset_url}'
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT)
        server.login(EMAIL_USER, EMAIL_PASS)
        text = msg.as_string()
        server.sendmail(EMAIL_USER, email, text)
        server.quit()
        print(f"Email enviado com sucesso para {email}")
        return True
    except Exception as e:
        print(f"Erro ao enviar email: {e}")
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
    connection = conectar()
    if not connection:
        return False
    try:
        user_id = readuser(email, table).readid(connection)
        edituser(user_id, "password", new_password, table).edit(connection)
        print(f"Senha atualizada com sucesso para {email}")
        return True
    except Exception as e:
        print(f"Erro ao atualizar senha: {e}")
        return False
    finally:
        connection.close()





#email verification


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
    msg['Subject'] = 'Confirme seu endereço de e-mail'

    body = f"""
    Olá, {name}!

    Obrigado por se cadastrar. Para ativar sua conta, clique no link abaixo:
    {confirm_url}

    Este link expira em 24 horas.
    """
    
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT)
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(EMAIL_USER, email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Erro ao enviar e-mail de confirmação: {e}")
        return False