from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from __init__ import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    """ For use in 'current_user' alone, to assign the 'current_user'
    to a variable and edit the user data use 'User.query.get' """
    user = User.query.get(int(user_id))
    db.session.remove()  # Closes the session to prevent max session overflow
    return user


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.png')
    motto = db.Column(db.String(200))
    bio = db.Column(db.String(1000))
    birthday = db.Column(db.DateTime())
    tasks = db.relationship('Tasks', backref='user', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        serialized = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return serialized.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        serialized = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = serialized.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Tasks(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    min_value = db.Column(db.Integer, nullable=False)
    max_value = db.Column(db.Integer, nullable=False)
    value = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.String(20), nullable=False)
    end_date = db.Column(db.String(20), nullable=False)
    public = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                        nullable=False)
