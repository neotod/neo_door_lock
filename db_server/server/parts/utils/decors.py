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
        if not current_app.config['TESTING']:
            path = request.path
            addr = request.remote_addr
            logger.info(f'New request: \n {path} \n {addr}\n')
        
        return func(*args, **kwargs)

    return wrapper

def check_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        checkers = [check_user_login, check_request_json, check_table_existence]
        for f in checkers:
            msg, status = f(request)
            if msg != 'ok':
                abort(make_response(msg, status))

        return func(*args, **kwargs)

    return wrapper