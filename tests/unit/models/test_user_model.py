from unittest import TestCase
from api.models import User

test_user_data = dict(
        email='Test@email', first_name='testfirstName', last_name='testLastName', password='test'
    )


class TestUserModel(TestCase):

    def test_very_passowrd(self):
        user_data = dict(test_user_data)
        password_hash = User.generate_hash(test_user_data['password'])
        user_data['password'] = password_hash
        user = User(**user_data)

        assert user.verify_password(test_user_data['password'])

    def test_serializer(self):
        user = User(**test_user_data).serialize()

        assert user['first_name'] == test_user_data['first_name']

    def test_representation(self):
        user = User(**test_user_data)

        assert repr(user) == f"<User: {test_user_data['first_name']} {test_user_data['last_name']}>"
