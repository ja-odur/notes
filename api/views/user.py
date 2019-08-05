from flask_restplus import Resource
from flask import request
from main import rest_api
from ..models.user import User
from ..utils.request_validators import validate_request_data, validate_json_request


@rest_api.route('/user')
class UserResource(Resource):

    @validate_json_request
    @validate_request_data(['email', 'password', 'first_name', 'last_name'])
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

    @validate_json_request
    @validate_request_data(['email', 'password'])
    def post(self):

        request_data = request.get_json()

        user = User.find_first(dict(email=request_data.get('email')))

        if user and user.verify_password(str(request_data.get('password'))):
            return (
                {
                    'status': 'success',
                    'token': user.token
                }, 200

            )

        return (

            {
                'status': 'error',
                'message': 'Invalid email or password',

            }, 401

        )
