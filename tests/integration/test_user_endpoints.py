from tests.test_base_case import BaseTestCase
import json

test_user_data = dict(
        email='Test@email.com', first_name='testfirstName', last_name='testLastName', password='test'
    )


class UserLoginEndpoints(BaseTestCase):

    def setUp(self):
        super().BaseSetUp()

    def test_login_succeeds(self):
        self.client().post("/api/v1/user", content_type="application/json", data=json.dumps(test_user_data))

        res = self.client().post("/api/v1/user/login", content_type="application/json", data=json.dumps(test_user_data))

        response = json.loads(res.data.decode('utf-8'))

        assert res.status_code == 200
        assert response['status'] == 'success'
