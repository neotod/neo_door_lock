import logging
from flask import current_app, g

from . import db


logger = logging.getLogger(__name__)

def validate_token(token):
    res = db.read_from_table(g.db_conn, 'api_tokens', None, {'token': token})

    if res:
        res = dict(res[0])
        user_id = res['user_id']

        res = db.read_from_table(g.db_conn, 'users', 'username', {'id': user_id})
        res = dict(res[0])
        username = res['username']
        
        return username
    else:
        return False

def check_user_login(request):
    if 'X-API-KEY' not in request.headers:
        msg = 'Please provide api key with "X-API-KEY" header, Or get a new api key by logging in (/login).\n'
        return msg, 401
    else:
        api_key = request.headers['X-API-KEY']
        username = validate_token(api_key)

        if username:
            if not current_app.config['TESTING']:
                logger.info(f'User {username} api key checked and was valid!')
            return 'ok', 200
        else:
            msg = 'Wrong api key! If you forget your api key you can get a new one by logging in (/login).\n'
            return msg, 401

def check_request_json(request):
    if not request.is_json and request.method == 'POST':
        return 'Please provide the JSON too!\n', 415
    else:
        return 'ok', 200

def validate_table_name(request):
    for tbl_name in request.get_json():
        if tbl_name in current_app.config['FORBIDDEN_TABLES']:
            msg = f"Table {tbl_name} can't be accessed!\n"
            return msg, 403

    return 'ok', 200