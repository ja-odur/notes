from pathlib import Path
from decouple import config as env_config
from dotenv import load_dotenv

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path, verbose=True)

class Config:
    """Base Application configurations"""
    MONGODB_SETTINGS = {
        'db': 'notes_project',
        'host': env_config('DATABASE_URL')
    }

    DEBUG = False
    TESTING = False

class ProductionConfig(Config):
    """Application production configurations"""


class DevelopmentConfig(Config):
    """Application development configurations"""

    DEBUG = True

class TestingConfig(Config):
    """Applications testing configuration"""

    TESTING = True
    MONGODB_SETTINGS = {
        'db': 'notes_project',
        'host': env_config('TEST_DATABASE_URL')
    }


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
