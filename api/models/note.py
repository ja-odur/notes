from .database import db
from .model_operations import ModelOperation
from .user import User


class Note(db.Document, ModelOperation):
    id = db.SequenceField(primary_key=True)
    title = db.StringField(required=True, max_length=80)
    email = db.EmailField(required=True)
    body = db.StringField(required=True)
    shared = db.ListField(db.ReferenceField(User))

    @classmethod
    def filter_by_shared(cls, *emails, **keywords):
        users = []
        for email in emails:
            user = User.find_first(dict(email=email))
            users.append(user) if user else None

        return cls.objects.filter(shared__in=users, **keywords).all()

    @classmethod
    def get_users(cls, *emails):
        users = []
        for email in emails:
            user = User.find_first(dict(email=email))
            users.append(user) if user else None
        return users

    @classmethod
    def filter_by_user(cls, email, **keywords):
        filter_dict = {'email': email}
        filter_dict.update(keywords) if keywords else None
        return list(cls.filter(filter_dict))  + list(cls.filter_by_shared(email, **keywords))

    def serialize(self):
        return dict(title=self.title, body=self.body, id=self.id)

    def update_note(self, data):
        self.update(**data)
        selfObj = self.serialize()
        if 'shared' in data.keys():
            shared = []

            for user in data.get('shared'):
                shared.append(user.serialize())
            data['shared'] = shared
        selfObj.update(data)
        return selfObj

    def __repr__(self):
        return '<Note: {}>'.format(self.title)
