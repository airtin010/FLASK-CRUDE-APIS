from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash


from CRUDEMANAGER.maindefs import conectar, createtable, deletetable, showtables,tablecontent, chosetable
from CRUDEMANAGER.add import useradd        
from CRUDEMANAGER.read import readuser




connection = conectar() # Conexão com o banco de dados

table = 'users'  # Nome da tabela onde os usuários estão armazenados

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
        
        if check_password_hash(readuser(email, table).readpassword(connection), password) and email == readuser(email, table).reademail(connection):
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

        passwordhash = generate_password_hash(password)

        if confirm_password != password:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('register'))

        elif email == readuser(email, table).reademail(connection):
            flash('Email already registered.', 'error')
            return redirect(url_for('register'))
        
        useradd(name, email, passwordhash, table).add(connection)
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('index.html')


    
@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    if request.method == 'POST':
        email = request.form['email']
        user = readuser(email, table).reademail(connection)
        if user:
            flash('Password reset link sent to your email.', 'success')
        else:
            flash('Email not found.', 'error')
        return redirect(url_for('forgot'))
    return render_template('forgot.html')


if __name__ == '__main__':
    with app.app_context():
        pass
    app.run(debug=True)