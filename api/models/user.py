from werkzeug.security import generate_password_hash, check_password_hash
from ..utils.token_generator import generate_token
from .database import db
from .model_operations import ModelOperation


class User(db.Document, ModelOperation):
    email = db.EmailField(required=True, primary_key=True)
    first_name = db.StringField(max_length=50)
    last_name = db.StringField(max_length=50)
    password = db.StringField(required=True, max_length=150)

    @classmethod
    def generate_hash(cls, password):

        return generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    @property
    def token(self):
        return generate_token(self.serialize())

    def serialize(self):
        return dict(email=self.email, first_name=self.first_name, last_name=self.last_name)

    def __repr__(self):
        return '<User: {} {}>'.format(self.first_name, self.last_name)







class UserDb:
    USERS = {}
    id = 0

    @classmethod
    def insert(cls, user):

        if user['name'] not in cls.USERS.keys():
            user.update({'id': cls.id})
            cls.USERS[user['name']] = dict(user)
            del user['password']
            cls.id += 1
            return cls.USERS[user['name']]
        return False

    @classmethod
    def get(cls, name):

        return cls.USERS.get(str(name), False)
