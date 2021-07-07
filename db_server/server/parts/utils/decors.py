import logging
from functools import wraps
from flask import (
    make_response, 
    current_app,
    request, 
    abort, 
)

from .etc import *


logger = logging.getLogger(__name__)

def log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        path = request.path
        addr = request.remote_addr
        logger.info(f'New request: \n {path} \n {addr}\n')
        
        return func(*args, **kwargs)

    return wrapper

def check_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        checkers = [check_user_login, check_request_json, validate_table_name]
        for f in checkers:
            msg, status = f(request)
            if msg != 'ok':
                abort(make_response(msg, status))

        return func(*args, **kwargs)

    return wrapper

def handle_bad_format(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            url_prefix = request.path[1:]
            format_key = url_prefix.replace('/', '-')
            msg = f'Please use the correct format for your JSON.\n For getting correct formats go to /format/{format_key}.\n'
            abort(make_response(msg, 422))

    return wrapper