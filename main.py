from flask import Flask
from flask_cors import CORS
from flask_restplus import Api
from api import api_blueprint

rest_api = Api(api_blueprint, doc=False)

def create_app():
    """creates a flask app object from a config object"""

    app = Flask(__name__)
    CORS(app)

    app.register_blueprint(api_blueprint)

    # import views
    import api.views



    return app