from flask import Flask ,jsonify
from flask_cors import CORS
from flask_restplus import Api
from api import api_blueprint, error_blueprint
from config import config as config_dict
from api.models.database import db
from api.utils.exceptions import ValidationError
from mongoengine.errors import ValidationError as MongoValidationError


rest_api = Api(api_blueprint, doc=False)


def create_app(config='production'):
    """creates a flask app object from a config object"""

    app = Flask(__name__)
    app.config.from_object(config_dict[config])
    CORS(app)
    db.init_app(app)

    app.register_blueprint(api_blueprint)
    app.register_blueprint(error_blueprint)

    # import views
    import api.views

    # import models
    import api.models



    return app


@rest_api.errorhandler(ValidationError)
@error_blueprint.app_errorhandler(ValidationError)
def handle_exception(error):
    """Error handler called when a ValidationError is raised"""

    return jsonify(error.error), 400

@rest_api.errorhandler(MongoValidationError)
@error_blueprint.app_errorhandler(MongoValidationError)
def handle_mongo_exception(error):
    """Error handler called when a ValidationError is raised"""
    try:
        errors = {
            key: value.message for key, value in error.errors.items()
        }
    except:
        return jsonify({'message': error.message}), 400

    return jsonify(errors), 400

