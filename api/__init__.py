from flask import Blueprint
api_blueprint = Blueprint('api_blueprint', __name__, url_prefix='/api/v1')
error_blueprint = Blueprint('error_blueprint', __name__)
