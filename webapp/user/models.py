from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from webapp.db import db


class User(db.Model, UserMixin):
    """
    Description of the table of registered users
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    surname = db.Column(db.String(50))
    email = db.Column(db.String(50), index=True, unique=True)
    password = db.Column(db.String(128))
    organization = db.Column(db.String(256))
    role = db.Column(db.String(10), index=True)
    tasks = db.relationship('Tasks', backref='tasks', lazy='dynamic')

    def set_password(self, password):
        """
        The function to set the hash for the user's password

        :param password: the user's password
        """
        self.password = generate_password_hash(password)

    def check_password(self, password) -> bool:
        """
        The function compares the password entered by the user
        with the registered hash for the user's password in the database

        :param password: the user's password
        :return: comparison result as boolean
        """
        return check_password_hash(self.password, password)

    @property
    def is_admin(self) -> bool:
        """
        The function checks if the user is an administrator

        :return: validation result as boolean
        """
        return self.role == 'admin'

    def __repr__(self) -> str:
        """
        This function displays on the command line the data of the user
        who has just logged into the application

        :return: string with username, surname and email
        """
        return '<User {} {}, email {}>'.format(self.username, self.surname, self.email)
