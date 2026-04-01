from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash

from CRUDEMANAGER.maindefs import conectar, createtable
from CRUDEMANAGER.crud.create import useradd        
from CRUDEMANAGER.crud.read import readuser
from email_reset import send_password_reset_email, verify_reset_token, update_password




connection = conectar() # Conexão com o banco de dados

table = 'databasedusers'  # Nome da tabela onde os usuários estão armazenados

#criar tabela users se não existir
createtable(connection, table)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'chave-secreta-local'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        stored_hash = readuser(email, table).readpassword(connection)
        if stored_hash and check_password_hash(stored_hash, password):
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password.', 'error')
            return redirect(url_for('login'))
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if confirm_password != password:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('register'))

        elif readuser(email, table).reademail(connection):
            flash('Email already registered.', 'error')
            return redirect(url_for('register'))
        
        useradd(name, email, password, table).add(connection)
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('index.html')


    
@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    if request.method == 'POST':
        email = request.form['email']
        if readuser(email, table).reademail(connection):
            if send_password_reset_email(email, app):
                flash('Password reset link sent to your email.', 'success')
            else:
                flash('Error sending email.', 'error')
        else:
            flash('Email not found.', 'error')
        return redirect(url_for('forgot'))
    return render_template('forgot.html')


@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    email = verify_reset_token(token)
    if not email:
        flash('Invalid or expired token.', 'error')
        return redirect(url_for('forgot'))
    if request.method == 'POST':
        new_password = request.form['password']
        confirm_password = request.form['confirm_password']
        if new_password != confirm_password:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('reset_password', token=token))
        if update_password(email, new_password, table):
            flash('Password updated successfully. Please log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Error updating password.', 'error')
    return render_template('reset_password.html')


if __name__ == '__main__':
    app.run(debug=True) 