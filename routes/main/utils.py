import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_login import current_user
from flask_mail import Message
from models import User
from flask import render_template as real_render_template


def render_template(*args, **kwargs):
    """ Takes all return_template calls and ensures they have the user_image
        I dont know a better way of doing this.
    """
    return real_render_template(*args, **kwargs, image_file=user_image())


def location(locator, picture_fn):
    if locator == 0:
        picture_path = os.path.join(
            current_app.root_path, 'static/profile_pics', picture_fn)
        output_size = (125, 125)
        return output_size, picture_path
    else:
        pass


def save_picture(form_picture, locator):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    output_size, picture_path = location(locator, picture_fn)

    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='simple.projects.help@gmail.com',
                  recipients=[user.email])
    url = url_for('users.reset_token', token=token, _external=True)

    msg.html = f'''\
<html>
    <head>
        <!-- Required meta tags -->
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    
        <!-- Bootstrap CSS -->
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    
        <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='main.css') }}">
    </head>
    <body>
        <section class="jumbotron text-center">
            <div class="container">
                <h1 class="jumbotron-heading">Simplified Projects</h1>
                <p class="lead text-muted"> 
                    This is an email about a password reset. If you did not send this request then ignore this email.
                </p>
                <a href="{ url }">Change Password</a> 
            </div>
        </section>
        <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
    </body>
</html>
'''

    mail.send(msg)


def user_image():
    try:
        image_file = url_for(
            'static', filename='profile_pics/' + current_user.image_file)
        return image_file
    except AttributeError:
        pass
