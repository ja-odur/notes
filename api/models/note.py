from .database import db
from .model_operations import ModelOperation


class Note(db.Document, ModelOperation):
    title = db.StringField(required=True, primary_key=True, max_length=80)
    body = db.StringField(required=True)
    shared = db.ListField()
