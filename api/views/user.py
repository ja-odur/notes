from flask_restplus import Resource
from flask import request
from main import rest_api
from ..models.user import UserDb, User
from ..utils.token_generator import generate_token
from ..utils.exceptions import ValidationError


@rest_api.route('/user')
class UserResource(Resource):

    def post(self):

        user_request_data = request.get_json()

        if User.find_first(dict(email=user_request_data['email'])):
            return (

                {
                    'status': 'error',
                    'message': f'user with {user_request_data["email"]} already exists',

                }, 400

            )

        user_request_data.update(dict(password=User.generate_hash(str(user_request_data['password']))))

        user = User(**user_request_data).save()

        return (

            {
                'status': 'success',
                'message': 'user created',
                'data': user.serialize()
            }, 201

        )

@rest_api.route('/user/login')
class UserLoginResource(Resource):

    def post(self):

        request_data = request.get_json()

        user = UserDb.get(request_data['name'])

        if user and request_data['password'] == user['password']:
            return (
                {
                    'status': 'success',
                    'token': generate_token(user)
                }, 200

            )

        return (

            {
                'status': 'error',
                'message': 'Invalid username or password',

            }, 401

        )


