from flask_restplus import Resource
from flask import request
from main import rest_api
from ..models.user import UserDb


@rest_api.route('/user')
class UserResource(Resource):

    def post(self):

        request_data = request.get_json()

        user = UserDb.insert(request_data)

        if user:
            return (

                {
                    'status': 'success',
                    'message': 'user created',
                    'data': user
                }, 201

            )

        return (

            {
                'status': 'error',
                'message': 'user not created',

            }, 200

        )

@rest_api.route('/user/login')
class UserLoginResource(Resource):

    def post(self):

        request_data = request.get_json()

        user = UserDb.get(request_data['name'])
        import pdb; pdb.set_trace()

        if user and request_data['password'] == user['password']:
            return (
                {
                    'status': 'success',
                    'token': 12345
                }, 200

            )

        return (

            {
                'status': 'error',
                'message': 'Invalid username or password',

            }, 401

        )


