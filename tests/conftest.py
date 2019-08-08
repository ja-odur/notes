import pytest
from main import create_app
from os import environ
from api.models import db


config_name = 'testing'
environ['APP_ENV'] = config_name
BASE_URL = '/api/v1'


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
