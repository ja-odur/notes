
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
