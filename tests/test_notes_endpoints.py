import json

class TestNotesEndpoints:

    def test_creating_note_succeeds(self, client, init_db, auth_header, note_data):
        res = client().post(
            "/api/v1/note",
            headers=auth_header,
            content_type="application/json",
            data=json.dumps(note_data)
        )

        response = json.loads(res.data.decode('utf-8'))

        assert res.status_code == 201
        assert response['status'] == 'success'

    def test_creating_note_with_missing_data_fails(self, client, init_db, auth_header, invalid_note_data):
        res = client().post(
            "/api/v1/note",
            headers=auth_header,
            content_type="application/json",
            data=json.dumps(invalid_note_data)
        )

        response = json.loads(res.data.decode('utf-8'))

        assert res.status_code == 400
        assert response['status'] == 'error'

    def test_creating_note_with_empty_data_fails(self, client, init_db, auth_header):
        res = client().post(
            "/api/v1/note",
            headers=auth_header,
            content_type="application/json",
            data=json.dumps({})
        )

        response = json.loads(res.data.decode('utf-8'))

        assert res.status_code == 400
        assert response['status'] == 'error'

    def test_creating_note_with_no_token_fails(self, client, init_db):
        res = client().post(
            "/api/v1/note",
            content_type="application/json",
            data=json.dumps({})
        )

        response = json.loads(res.data.decode('utf-8'))

        assert res.status_code == 400
        assert response['status'] == 'error'

    def test_creating_note_with_token_missing_bearer_prefix_fails(self, client, init_db, invalid_auth_header):
        header = dict(invalid_auth_header)
        header['Authorization'].format('missing_prefix')
        res = client().post(
            "/api/v1/note",
            headers=header,
            content_type="application/json",
            data=json.dumps({})
        )

        response = json.loads(res.data.decode('utf-8'))

        assert res.status_code == 400
        assert response['status'] == 'error'

    def test_creating_duplicate_note_fails(self, client, init_db, auth_header, note_data):
        res = client().post(
            "/api/v1/note",
            headers=auth_header,
            content_type="application/json",
            data=json.dumps(note_data)
        )

        response = json.loads(res.data.decode('utf-8'))

        assert res.status_code == 400
        assert response['status'] == 'error'

    def test_getting_note_succeeds(self, client, init_db, auth_header):
        res = client().get(
            "/api/v1/note",
            headers=auth_header,
        )

        response = json.loads(res.data.decode('utf-8'))

        assert res.status_code == 200
        assert response['status'] == 'success'

    def test_getting_single_note_succeeds(self, client, init_db, auth_header, note):
        new_note = note.save()
        res = client().get(
            f"/api/v1/note/{new_note.id}",
            headers=auth_header,
        )

        response = json.loads(res.data.decode('utf-8'))

        assert res.status_code == 200
        assert response['status'] == 'success'

    def test_getting_single_note_with_invalid_fails(self, client, init_db, auth_header):

        res = client().get(
            f"/api/v1/note/{1324}",
            headers=auth_header,
        )

        response = json.loads(res.data.decode('utf-8'))

        assert res.status_code == 404
        assert response['status'] == 'error'

    def test_updating_note_succeeds(self, client, init_db, auth_header, note, note_data):
        new_note = note.save()
        res = client().patch(
            f"/api/v1/note/{new_note.id}",
            headers=auth_header,
            data=json.dumps(note_data)
        )

        response = json.loads(res.data.decode('utf-8'))

        assert res.status_code == 200
        assert response['status'] == 'success'

    def test_patching_single_note_with_invalid_fails(self, client, init_db, auth_header, note_data):
        res = client().patch(
            f"/api/v1/note/{1324}",
            headers=auth_header,
            data=json.dumps(note_data)
        )

        response = json.loads(res.data.decode('utf-8'))

        assert res.status_code == 404
        assert response['status'] == 'error'

