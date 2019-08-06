from unittest import TestCase
from api.models import User

test_user_data = dict(
        email='Test@email', first_name='testfirstName', last_name='testLastName', password='test'
    )


class TestUserModel(TestCase):

    def test_representation(self):
        user = User(**test_user_data)

        assert repr(user) == f"<User: {test_user_data['first_name']} {test_user_data['last_name']}>"
