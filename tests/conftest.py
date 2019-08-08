import pytest
from main import create_app
from os import environ
from faker import Faker
from api.models import db, User, Note


config_name = 'testing'
environ['APP_ENV'] = config_name
BASE_URL = '/api/v1'

fake = Faker()


@pytest.yield_fixture(scope='session')
def app():
    """
    Setup our flask test app, this only gets executed once.
    :return: Flask app
    """
    _app = create_app(config_name)

    # Establish an application context before running the tests.
    ctx = _app.app_context()
    ctx.push()

    yield _app

    ctx.pop()

@pytest.fixture(scope='function')
def client(app):
    """
    Setup an app client, this gets executed for each test function.
    :param app: Pytest fixture
    :return: Flask app client
    """
    yield app.test_client


@pytest.fixture(scope='module')
def init_db(app):
    yield db
    db.connection.drop_database('noteDBtest')

@pytest.fixture(scope='module')
def user():
    user_data = {
        'first_name': fake.first_name(),
        'last_name': fake.first_name(),
        'email': fake.email(),
        'password': fake.password()
    }

    return User(**user_data)

@pytest.fixture(scope='module')
def user2():
    user_data = {
        'first_name': fake.first_name(),
        'last_name': fake.first_name(),
        'email': fake.email(),
        'password': fake.password()
    }

    return User(**user_data), user_data

@pytest.fixture(scope='module')
def note_data(user2):
    user2, user2_data = user2
    user2.save()
    return {
        'body': fake.paragraph(),
        'title': fake.sentence(),
        'shared': [user2_data.get('email')]
    }

@pytest.fixture(scope='module')
def note(user):

    note = {
        'body': fake.paragraph(),
        'title': fake.sentence(),
        'email': user.email
    }

    return Note(**note)

@pytest.fixture(scope='module')
def invalid_note_data(user):

    return  {
        'body': fake.paragraph(),

        'email': user.email
    }

@pytest.fixture(scope='module')
def auth_header(user):
    return {
        'Authorization': f'bearer {user.token}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

@pytest.fixture(scope='module')
def invalid_auth_header(user):
    return {
        'Authorization': '{}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
