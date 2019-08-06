from unittest import TestCase
from main import create_app
from os import environ
from api.models import db

config_name = 'testing'
environ['APP_ENV'] = config_name


class BaseTestCase(TestCase):

    def BaseSetUp(self):
        """Define test variables and initialize app"""
        self.app = create_app('testing')
        self.client = self.app.test_client
        self.app.testing = True
        with self.app.app_context():
            db.connection.drop_database('noteDBtest')
