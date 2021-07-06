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

def check_table_existence(request):
    table_name = request.path.split('/')[-1]

    try:
        list(db.get_table_columns(g.db_conn, table_name)) # a test to check if the table exists
    except ValueError:
        return 'Provided table name is wrong!\n', 422
    else:
        return 'ok', 200