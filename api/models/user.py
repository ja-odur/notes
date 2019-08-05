
class UserDb:
    USERS = {}
    id = 0

    @classmethod
    def insert(cls, user):

        if user['name'] not in cls.USERS.keys():
            user.update({'id': cls.id})
            cls.USERS[user['name']] = user
            del user['password']
            return cls.USERS[user['name']]
        return False
