from .database import db
from .model_operations import ModelOperation


class Note(db.Document, ModelOperation):
    id = db.SequenceField(primary_key=True)
    title = db.StringField(required=True, max_length=80)
    email = db.EmailField(required=True)
    body = db.StringField(required=True)
    shared = db.ListField()

    def serialize(self):
        return dict(title=self.title, body=self.body, id=self.id)

    def __repr__(self):
        return '<Note: {}>'.format(self.title)
