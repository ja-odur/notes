import json

test_user_data = dict(
        email='Test@email.com', first_name='testfirstName', last_name='testLastName', password='test'
    )

invalid_test_user_data = dict(
        email='Test@email.com', first_name='testfirstName', last_name='testLastName', password='invalid_password'
    )


class TestUserLoginEndpoints:

    def test_signup_succeeds(self, client, init_db):
        res = client().post("/api/v1/user", content_type="application/json", data=json.dumps(test_user_data))



        response = json.loads(res.data.decode('utf-8'))

        assert res.status_code == 201
        assert response['status'] == 'success'

    def test_duplicate_signup_fails(self, client, init_db):
        res = client().post("/api/v1/user", content_type="application/json", data=json.dumps(invalid_test_user_data))

        response = json.loads(res.data.decode('utf-8'))

        assert res.status_code == 400
        assert response['status'] == 'error'

    def test_login_succeeds(self, client, init_db):
        res = client().post("/api/v1/user/login", content_type="application/json", data=json.dumps(test_user_data))


        response = json.loads(res.data.decode('utf-8'))

        assert res.status_code == 200
        assert response['status'] == 'success'


    def test_login_with_invalid_data_fails(self, client, init_db):
        res = client().post(
            "/api/v1/user/login",
            content_type="application/json",
            data=json.dumps(invalid_test_user_data))


        response = json.loads(res.data.decode('utf-8'))

        assert res.status_code == 401
        assert response['status'] == 'error'