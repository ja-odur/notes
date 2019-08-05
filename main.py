from flask import Flask
from flask_cors import CORS
from flask_restplus import Api
from api import api_blueprint
from api.utils.exceptions import ValidationError

rest_api = Api(api_blueprint, doc=False)

def create_app():
    """creates a flask app object from a config object"""

    app = Flask(__name__)
    CORS(app)

    app.register_blueprint(api_blueprint)

    # import views
    import api.views



    return app


@rest_api.errorhandler(ValidationError)
def handle_exception(error):
    """Error handler called when a ValidationError is raised"""

    return jsonify(error.error), 400