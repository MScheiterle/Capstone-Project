from __init__ import bcrypt
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from models import User
from wtforms import BooleanField, PasswordField, StringField, SubmitField, DateField, TextAreaField, TelField
from wtforms.validators import (DataRequired, Email, EqualTo, Length,
                                ValidationError, Optional)


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


def password_validation(form, field):
    if not form.confirm_password.data == form.new_password.data:
        raise ValidationError(
            'Confirm Password must match New Password')
    if (not form.old_password.data) and form.new_password.data:
        raise ValidationError(
            'Please verify you are the owner by inputting your old password')
    if form.old_password.data and not form.new_password.data:
        raise ValidationError(
            'Input the new password you want to use')
    if form.old_password.data and not bcrypt.check_password_hash(current_user.password, form.old_password.data):
        raise ValidationError(
            'The current password does not match the password on record.')


class UpdateAccountInfoForm(FlaskForm):
    username = StringField('Username',
                           validators=[Length(min=2, max=20)])
    email = StringField('Email', validators=[
                        Optional(), Email(), Length(min=10, max=80)])
    secondary_email = StringField('Alternative Email', validators=[
        Optional(), Email(), Length(min=0, max=80)])
    picture = FileField('Update Profile Picture', validators=[Optional(),
                        FileAllowed(['jpg', 'png', 'jpeg'])])
    motto = TextAreaField('Motto',
                          validators=[Optional(), Length(min=0, max=200)])
    bio = TextAreaField('Bio',
                        validators=[Optional(), Length(min=0, max=1000)])
    birthday = DateField('Birthday',
                         validators=[Optional()])
    telephone_number = TelField('Telephone Number',
                                validators=[Optional()], render_kw={"placeholder": "123-4567-8901", "pattern": "[0-9]{3}-[0-9]{3}-[0-9]{4}"})
    old_password = PasswordField('Current Password',
                                 validators=[Optional(), password_validation, Length(min=8)])
    new_password = PasswordField('New Password',
                                 validators=[Optional(), password_validation, Length(min=8)])
    confirm_password = PasswordField('Confirm New Password',
                                     validators=[Optional(), password_validation, Length(min=8)])
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

    def validate_telephone_number(self, telephone_number):
        if telephone_number.data != current_user.email:
            user = User.query.filter_by(email=telephone_number.data).first()
            if user:
                raise ValidationError(
                    'That telephone number is taken. Please choose a different one.')
