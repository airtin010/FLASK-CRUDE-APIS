from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from functools import wraps
from datetime import timedelta

from CRUDEMANAGER.maindefs import connect, create_table
from CRUDEMANAGER.crud.create import UserAdd        
from CRUDEMANAGER.crud.read import UserRead
from CRUDEMANAGER.crud.update import UserEdit
from email_defs import send_password_reset_email, verify_reset_token, update_password, verify_confirmation_token, send_verification_email

connection = connect()
table = 'databasedusers'
create_table(connection, table)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'local-secret-key'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Restricted access. Please log in.", "error")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user_reader = UserRead(email, table)
        stored_hash = user_reader.read_password(connection)
        
        if stored_hash and check_password_hash(stored_hash, password):
            if user_reader.is_verified(connection):
                session.permanent = True
                session['user_email'] = email
                session['user_id'] = user_reader.read_id(connection)
                flash('Login successful!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Email not verified. Please check your inbox.', 'error')
                return redirect(url_for('login'))
        else:
            flash('Invalid email or password.', 'error')
            return redirect(url_for('login'))
        
    return render_template('login.html')

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
        elif UserRead(email, table).read_email(connection):
            flash('Email already registered.', 'error')
            return redirect(url_for('register'))
        
        UserAdd(name, email, password, table).add(connection)
        send_verification_email(email, name)
        flash('Registration successful. Please check your email for the verification link.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')
    
@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    if request.method == 'POST':
        email = request.form['email']
        if UserRead(email, table).read_email(connection):
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

@app.route('/confirm/<token>')
def confirm_email(token):
    email = verify_confirmation_token(token)
    if email is None:
        return "The confirmation link is invalid or has expired.", 400
    
    user_id = UserRead(email, table).read_id(connection)
    UserEdit(user_id, "verification_token", "verified", table).update(connection)
    
    return "Email confirmed successfully! You can now log in."

if __name__ == '__main__':
    app.run(debug=True)