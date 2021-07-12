import logging
from flask import g

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