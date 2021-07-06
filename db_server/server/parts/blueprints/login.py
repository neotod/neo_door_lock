import os
import time
import logging
from hashlib import sha256
from flask import (
    make_response, 
    current_app,
    Blueprint, 
    request, 
    abort, 
    g, 
)
from flask.json import jsonify

from ..utils.decors import log
from ..utils import db

logger = logging.getLogger(__name__)
bp = Blueprint('login', __name__)

@bp.route('/login', methods=['POST'])
@log
def login():
    msg = ''
    if request.form:
        if 'username' not in request.form:
            msg += 'Please provide your Username!\n'
        if 'password' not in request.form:
            msg += 'Please provide your Password!\n'
    else:
        msg += 'Please provide your Username!\n'
        msg += 'Please provide your Password!\n'

    if msg:
        abort(make_response(msg, 401))
        
    username = request.form['username']
    password = request.form['password']

    res = db.read_from_table(g.db_conn, 'users', None, {'username': username})
    if res:
        res = dict(res[0])

        user_id = res['id']
        hash_id = res['pass_hash_id']

        res = db.read_from_table(g.db_conn, 'pass_hashes', 'hash', {'id': hash_id})
        real_pass_hash = dict(res[0])['hash']
        pass_hash = sha256(password.encode()).hexdigest()

        if real_pass_hash == pass_hash:
            revoke_token = False
            res = db.read_from_table(g.db_conn, 'api_tokens', 'user_id', {'user_id': user_id})
            if res:
                revoke_token = True

            token = sha256(os.urandom(16) + str(time.time()).encode()).hexdigest() # hope it's secure :)

            if revoke_token:
                res = db.update_table(g.db_conn, 'api_tokens', {'token': token}, {'user_id': user_id})
            else:
                res = db.insert_into_table(g.db_conn, 'api_tokens', ('user_id', 'token'), (user_id, token))

            if res:
                return jsonify(username=username, token=token)
            else:
                if not current_app.config['TESTING']:
                    logger.error(f'Login info: \n\t username: {username}')

                return make_response('Failed!\n', 500)
        else:
            return make_response('Password is wrong!\n', 401)

    else:
        return make_response('Username is wrong!\n', 401)