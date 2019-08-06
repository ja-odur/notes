from flask_restplus import Resource
from flask import request
from main import rest_api
from ..models import Note
from ..utils import validate_request_data, validate_json_request, token_required



@rest_api.route('/note')
class NoteResource(Resource):

    @token_required
    @validate_json_request
    @validate_request_data(['title', 'body'])
    def post(self, current_user):

        print('current', current_user)

        note_request_data = request.get_json()

        if Note.find_first(dict(title=note_request_data['title'])):
            return (

                {
                    'status': 'error',
                    'message': f'Note with title {note_request_data["title"]} already exists',

                }, 400

            )

        note_request_data.update(dict(email=current_user.get('UserInfo').get('email')))

        note = Note(**note_request_data).save()

        return (

            {
                'status': 'success',
                'message': 'Note created',
                'data': note.serialize()
            }, 201

        )
