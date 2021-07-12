import os
import logging
from flask import (
    make_response,
    Blueprint, 
    send_file,
    request, 
    g, 
)
from flask.json import jsonify

from ..utils import db
from ..utils.decors import *

logger = logging.getLogger(__name__)
bp = Blueprint('db', __name__, url_prefix='/db')

@bp.route('/read', methods=['POST'])
@must_authenticate
@json_required
@check_bad_format
def table_read():
    limit = 50
    conditions = None

    results = {}
    data = request.get_json()
    for tbl_name in data:
        tbl_data = data[tbl_name]

        if 'limit' in tbl_data:
            limit = tbl_data['limit']

        if 'conditions' in tbl_data:
            conditions = tbl_data['conditions']
        
        res = db.read_from_table(g.db_conn, tbl_name, None, conditions)
        if res:
            results[tbl_name] = [dict(r) for r in res[:limit]]
        else:
            results[tbl_name] = []

    if results:
        return jsonify(result=results)
    else:
        logger.error(f'Table info: \n\t connection: {g.db_conn} \n\t data: {data}')

        return make_response('Failed!\n', 500)

@bp.route('/insert', methods=['POST'])
@must_authenticate
@json_required
@check_bad_format
def table_insert():
    data = request.get_json()

    results = {}
    for tbl_name in data.keys():
        results[tbl_name] = 'success'

        tbl_data = data[tbl_name]
        cols = tbl_data['cols']
        vals = tbl_data['vals']

        res = db.insert_into_table(g.db_conn, tbl_name, cols, vals)

        if not res:
            results[tbl_name] = 'failed'

    if results:
        return jsonify(result=results)
    else:
        logger.error(f'DB_Connection: {g.db_conn} \n\t data: {data}')

        return make_response('Failed!\n', 500)

@bp.route('/update', methods=['POST'])
@must_authenticate
@json_required
@check_bad_format
def table_update():
    data = request.get_json()

    results = {}
    for tbl_name in data.keys():
        results[tbl_name] = []
        
        tbl_datas = data[tbl_name]
        for tbl_data in tbl_datas:
            results[tbl_name].append('success')

            setting_cols = tbl_data['setting_cols']
            conditions = None
            if 'condition' in tbl_data:
                conditions = tbl_data['conditions']

            res = db.update_table(g.db_conn, tbl_name, setting_cols, conditions)
            
            if not res:
                results[tbl_name][-1] = 'failed'

    if results:
        return jsonify(result=results)
    else:
        logger.error(f'DB_Connection: {g.db_conn} \n\t data: {data}')

        return make_response('Failed!\n', 500)

@bp.route('/delete', methods=['POST'])
@must_authenticate
@json_required
@check_bad_format
def table_delete():
    data = request.get_json()

    results = {}
    for tbl_name in data.keys():
        results[tbl_name] = []

        conditions = data[tbl_name]
        for condi in conditions:
            res = db.delete_from_table(g.db_conn, tbl_name, condi)

            if res:
                results[tbl_name].append('success')
            else:
                results[tbl_name].append('failed')

    if results:
        return jsonify(result=results)
    else:
        logger.error(f'DB_Connection: {g.db_conn} \n\t data: {data}')

        return make_response('Failed!\n', 500)

@bp.route('/backup')
@just_allow(['admin', 'bot'])
@must_authenticate
def backup():
    return send_file(os.path.join(os.pardir, current_app.config['DB_PATH']), download_name='backup.db', mimetype='application/vnd.sqlite3', as_attachment=True)