from __init__ import bcrypt, db
from flask import Blueprint, flash, redirect, request, url_for, render_template
from flask_login import current_user, login_user, logout_user
from models import User

from routes.main.forms import (LoginForm, RegistrationForm, RequestResetForm,
                               ResetPasswordForm)
from routes.main.utils import send_reset_email

main = Blueprint("main", __name__)


@main.route("/", methods=["GET", "POST"])
async def homepage():
    return render_template("homepage.html")


@main.route("/login", methods=["GET", "POST"])
async def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.homepage"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            db.session.remove()
            return (
                redirect(next_page) if next_page else redirect(
                    url_for("main.homepage"))
            )
        elif not user:
            flash("There is no account with that name", "warning")
        else:
            flash("Username and Password do not match", "warning")
    return render_template("login.html", title="Login", form=form)


@main.route("/logout", methods=["GET", "POST"])
async def logout():
    logout_user()
    return redirect(url_for("main.homepage"))


@main.route("/register", methods=["GET", "POST"])
async def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.homepage"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user = User(
            username=form.username.data, email=form.email.data, password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        user = User.query.filter_by(username=form.username.data).first()
        login_user(user)
        return redirect(url_for("main.login"))
    return render_template("register.html", title="Register", form=form)


@main.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@main.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)


@main.route("/account", methods=["GET", "POST"])
async def account():
    if not current_user.is_authenticated:
        flash("Please Log In First", "error")
        return redirect(url_for("main.homepage"))
    return render_template("account.html", title="Account")
