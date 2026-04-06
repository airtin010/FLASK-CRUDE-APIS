from datetime import timedelta
from functools import wraps

from flask import Flask, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash

from CRUDEMANAGER.maindefs import connect, create_table, is_password_strong
from CRUDEMANAGER.crud.create import UserAdd
from CRUDEMANAGER.crud.read import UserRead
from CRUDEMANAGER.crud.update import UserEdit
from email_defs import (
    send_password_reset_email,
    send_verification_email,
    update_password,
    verify_confirmation_token,
    verify_reset_token,
)

connection = connect()
TABLE_NAME = "databasedusers"
create_table(connection, TABLE_NAME)

app = Flask(__name__)
app.config["SECRET_KEY"] = "local-secret-key"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=7)


def render_auth_form(**context):
    return render_template("login_register.html", **context)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Restricted access. Please log in.", "error")
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return decorated_function


@app.route("/")
@login_required
def index():
    return render_template("index.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user_reader = UserRead(email, TABLE_NAME)
        stored_hash = user_reader.read_password(connection)

        if stored_hash and check_password_hash(stored_hash, password):
            if user_reader.is_verified(connection):
                session.permanent = True
                session["user_email"] = email
                session["user_id"] = user_reader.read_id(connection)
                flash("Login successful!", "success")
                return redirect(url_for("index"))

            flash("Email not verified. Please check your inbox.", "error")
            return redirect(url_for("login"))

        flash("Invalid email or password.", "error")
        return redirect(url_for("login"))

    return render_auth_form()


@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")
    confirm_password = request.form.get("confirm_password", "")

    if confirm_password != password:
        flash("Passwords do not match.", "error")
        return render_auth_form(name=name, email=email)

    is_valid, message = is_password_strong(password)
    if not is_valid:
        flash(message, "error")
        return render_auth_form(name=name, email=email)

    user_exists = UserRead(email, TABLE_NAME).read_email(connection)

    if user_exists:
        flash("Email already registered.", "error")
        return render_auth_form(name=name, email=email)

    try:
        UserAdd(name, email, password, TABLE_NAME).add(connection)
        send_verification_email(email, name)
        flash("Registration successful! Please check your email.", "success")
        return redirect(url_for("login"))
    except Exception as error:
        flash(f"Error during registration: {error}", "error")
        return render_auth_form(name=name, email=email)


@app.route("/forgot", methods=["GET", "POST"])
def forgot():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        if UserRead(email, TABLE_NAME).read_email(connection):
            if send_password_reset_email(email):
                flash("Password reset link sent to your email.", "success")
            else:
                flash("Error sending email.", "error")
        else:
            flash("Email not found.", "error")
        return redirect(url_for("forgot"))
    return render_template("forgot.html")


@app.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    email = verify_reset_token(token)
    if not email:
        flash("Invalid or expired token.", "error")
        return redirect(url_for("forgot"))

    if request.method == "POST":
        new_password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if new_password != confirm_password:
            flash("Passwords do not match.", "error")
            return redirect(url_for("reset_password", token=token))

        is_valid, message = is_password_strong(new_password)
        if not is_valid:
            flash(message, "error")
            return redirect(url_for("reset_password", token=token))

        if update_password(email, new_password, TABLE_NAME):
            flash("Password updated successfully. Please log in.", "success")
            return redirect(url_for("login"))

        flash("Error updating password.", "error")

    return render_template("reset_password.html")


@app.route("/confirm/<token>")
def confirm_email(token):
    email = verify_confirmation_token(token)
    if email is None:
        flash("The confirmation link is invalid or has expired.", "error")
        return redirect(url_for("login"))

    user_id = UserRead(email, TABLE_NAME).read_id(connection)
    UserEdit(user_id, "verification_token", "verified", TABLE_NAME).update(connection)

    flash("Email confirmed successfully! You can now log in.", "success")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
