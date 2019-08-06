from flask import request
from functools import wraps
import jwt
from decouple import config
from base64 import b64decode
from .exceptions import ValidationError

def token_required(func):

    @wraps(func)
    def decorated(*args, **kwargs):
        token = get_token()

        try:
            current_user = jwt.decode(
                token,
                b64decode(config('JWT_PUBLIC_KEY')).decode('utf8'),
                algorithms=['RS256'],
                options={
                    'verify_signature': True,
                    'verify_exp': True
                })
        except (ValueError, TypeError, jwt.ExpiredSignatureError,
                jwt.DecodeError, jwt.InvalidSignatureError):
            raise ValidationError({'message': 'Invalid token'})

        self, *args = args

        return func(self, current_user, *args, **kwargs)

    return decorated


def generate_token(user, exp=None):
    payload = {
        'UserInfo': user,
    }
    payload.__setitem__('exp', exp) if exp is not None else ''

    token = jwt.encode(payload, b64decode(config('JWT_PRIVATE_KEY')).decode('utf8'), algorithm='RS256').decode('utf-8')
    return token


def get_token(http_request=request):
    """Get token from request object

    Args:
        http_request (HTTPRequest): Http request object

    Returns:
        token (string): Token string

    Raises:
        ValidationError: Validation error raised when there is no token
                         or bearer keyword in authorization header
    """
    token = http_request.headers.get('Authorization')
    if not token:
        raise ValidationError({'message': 'No authorization token supplied'}, 401)
    elif 'bearer' not in token.lower():
        raise ValidationError({'message': "token does is no prefix with 'bearer'"}, 401)
    token = token.split(' ')[-1]
    return token