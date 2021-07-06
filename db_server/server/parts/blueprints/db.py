import logging
from flask import (
    make_response,
    current_app,
    Blueprint, 
    request, 
    abort,
    g, 
)
from flask.json import jsonify

from ..utils import db
from ..utils.decors import check_errors, log

logger = logging.getLogger(__name__)
bp = Blueprint('db', __name__, url_prefix='/db')

@bp.route('/read/<table_name>', methods=['GET', 'POST'])
@check_errors
@log
def table_read(table_name):
    limit = 50
    conditions = None
    if request.is_json:
        data = request.get_json()

        if 'limit' in data:
            limit = data['limit']

        if 'conditions' in data:
            conditions = data['conditions']
        
    result = db.read_from_table(g.db_conn, table_name, None, conditions)

    if result:
        result = [dict(r) for r in result[:limit]]
        return jsonify(result=result,)

    else:
        if not current_app.config['TESTING']:
            logger.error(f'Table info: \n\t connection: {g.db_conn} \n\t name: {table_name}\n\t data: {data}')

        return make_response('Failed!\n', 500)

@bp.route('/insert/<table_name>', methods=['POST'])
@check_errors
@log
def table_insert(table_name):
    data = request.get_json()
    cols = data['cols']
    vals = data['vals']
    
    res = db.insert_into_table(g.db_conn, table_name, cols, vals)
    
    if res:
        return make_response('Success\n', 200)
    else:
        if not current_app.config['TESTING']:
            logger.error(f'Table info: \n\t connection: {g.db_conn} \n\t name: {table_name}')

        return make_response('Failed!\n', 500)