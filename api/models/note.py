from .database import db
from .model_operations import ModelOperation


class Note(db.Document, ModelOperation):
    title = db.StringField(required=True, primary_key=True, max_length=80)
    email = db.EmailField(required=True)
    body = db.StringField(required=True)
    shared = db.ListField()

    def serialize(self):
        return dict(title=self.title, body=self.body)

    def __repr__(self):
        return '<Note: {}>'.format(self.title)
