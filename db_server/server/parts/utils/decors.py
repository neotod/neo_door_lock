from functools import wraps
from flask import (
    make_response, 
    current_app,
    request, 
    abort, 
)

from .etc import *

def must_authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'X-API-KEY' not in request.headers:
            msg = 'Please provide api key with "X-API-KEY" header, Or get a new api key by logging in (/login).\n'
            return make_response(msg, 401)
        else:
            api_key = request.headers['X-API-KEY']
            username = validate_token(api_key)

            if not username:
                msg = 'Wrong api key! If you forget your api key you can get a new one by logging in (/login).\n'
                return make_response(msg, 401)

        return func(*args, **kwargs)
    return wrapper

def just_allow(usernames):
    def outer(func): # assuming that user have been authenticated
        @wraps(func)
        def inner(*args, **kwargs):
            api_key = request.headers['X-API-KEY']
            username = validate_token(api_key)
            if username not in usernames:
                for tbl_name in request.get_json():
                    if tbl_name in current_app.config['FORBIDDEN_TABLES']:
                        msg = f"Table {tbl_name} can't be accessed!\n"
                        return make_response(msg, 403)

                if request.path == '/db/backup':
                    msg = "You can't access this URL."
                    return make_response(msg, 403)

            return func(*args, **kwargs)
        return inner
    return outer

def check_bad_format(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            url_prefix = request.path[1:]
            format_key = url_prefix.replace('/', '-')
            msg = f'Please use the correct format for your JSON.\n For getting correct formats go to /format/{format_key}.\n'
            abort(make_response(msg, 422))

    return wrapper

def json_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not request.is_json and request.method == 'POST':
            return 'Please provide the JSON too!\n', 415
        else:
            return func(*args, **kwargs)

    return wrapper