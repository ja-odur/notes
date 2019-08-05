from functools import wraps
from .exceptions import ValidationError
from flask import request

def validate_json_request(func):
    """Decorator function to check for json content type in request"""

    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not request.is_json:
            raise ValidationError(
                {
                    'status': 'error',
                    'message': 'json data required'
                }, 400)
        return func(*args, **kwargs)

    return decorated_function


def validate_request_data(keys):

    def validate_request(func):

        @wraps(func)
        def decorated(*args, **kwargs):
            errors = {}
            for key in keys:

                if key not in request.get_json().keys():
                    errors[key] = f'{key} is required'

            if errors:
                raise ValidationError({'message': errors})

            return func(*args, **kwargs)

        return decorated

    return validate_request


