from flask_restplus import Resource
from flask import request
from main import rest_api
from ..models import Note, User
from ..utils import validate_request_data, validate_json_request, token_required, response_msg


@rest_api.route('/note')
class NoteResource(Resource):

    @token_required
    @validate_json_request
    @validate_request_data(['title', 'body'])
    def post(self, current_user):

        note_request_data = request.get_json()

        if note_request_data.get('shared', []):
            shared = []
            for user_email in note_request_data.get('shared'):
                user = User.find_first(dict(email=user_email))
                shared.append(user) if user else None
            note_request_data['shared'] = shared

        if Note.find_first(dict(title=note_request_data['title'], email=current_user.get('UserInfo').get('email'))):
            return response_msg(
                'error',
                message=f'Note with title {note_request_data["title"]} already exists',
            )

        note_request_data.update(dict(email=current_user.get('UserInfo').get('email')))

        note = Note(**note_request_data).save()

        return response_msg(
            'success',
            message='Note created',
            payload=dict(note=note.serialize()),
            http_status=201
        )

    @token_required
    def get(self, current_user):

        notes = [
            note.serialize() for note in Note.filter_by_user(current_user.get('UserInfo').get('email'))
        ]

        return response_msg(
            'success',
            payload=notes,
            http_status=200
        )


@rest_api.route('/note/<int:note_id>')
class SingleNoteResource(Resource):

    @token_required
    def get(self, current_user, note_id):
        note = Note.filter_by_user(current_user.get('UserInfo').get('email'), id=note_id)

        if not note:
            return response_msg(
                'error',
                message='Note not found',
                http_status=404
            )

        return response_msg(
            'success',
            payload=note[0].serialize(),
            http_status=200
        )

    @token_required
    def patch(self, current_user, note_id):

        update_request_data = request.get_json()

        note = Note.filter_by_user(current_user.get('UserInfo').get('email'), id=note_id)

        if not note:
            return response_msg(
                'error',
                message='Note not found',
                http_status=404
            )

        if 'shared' in update_request_data.keys():
            update_request_data['shared'] = Note.get_users(*update_request_data.get('shared'))

            if note[0].email != current_user.get('UserInfo').get('email'):
                return response_msg(
                    'error',
                    message='Note authorized to edit the "shared" attribute of the note',
                    http_status=403
                )

        note = note[0].update_note(update_request_data)

        return response_msg(
            'success',
            message='Note updated successfully',
            payload=note,
            http_status=200
        )







