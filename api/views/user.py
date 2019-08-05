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

