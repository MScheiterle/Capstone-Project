from __init__ import bcrypt
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from models import User
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import (DataRequired, Email, EqualTo, Length,
                                ValidationError)


class RegistrationForm(FlaskForm):
    """ Define the registartion form """
    username = StringField('Username',
                           validators=[DataRequired()])
    email = StringField('Email',
                        validators=[Email()])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        """ Validates that a username is a username """
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'That username is taken. Please choose a different one.')

    def validate_email(self, email):
        """ Validates that an email is an email """
        if email.data is not '':
            # All User.query.filter_by need to share a function then check if has tables or not. If it doesnt it needs to call OperationalErrorcreate_dev_tables()
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    'That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    """ Defines a login form """
    username = StringField('Username',
                           validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class ResetPasswordForm(FlaskForm):
    """ Defines an update password form """
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=12)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError(
                'There is no account with that email. You must register first.')


class UpdateAccountInfoForm(FlaskForm):
    username = StringField('Username',
                           validators=[Length(min=2, max=20)])
    email = StringField('Email', validators=[Email()])
    picture = FileField('Update Profile Picture', validators=[
                        FileAllowed(['jpg', 'png', 'jpeg'])])
    old_password = PasswordField('Old Password')
    new_password = PasswordField('New Password')
    confirm_password = PasswordField('Confirm New Password',
                                     validators=[EqualTo('new_password')])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    'That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    'That email is taken. Please choose a different one.')

    def validate_old_password(self, old_password):
        if old_password.data and not bcrypt.check_password_hash(current_user.password, old_password.data):
            raise ValidationError(
                'That does not match your password')

    def validate_new_password(self, new_password):
        if self.old_password.data:
            if not len(new_password.data) >= 8:
                raise ValidationError(
                    'Your password must be atleast 8 characters long')
            if not new_password.data:
                raise ValidationError(
                    'You need to input a new password')
