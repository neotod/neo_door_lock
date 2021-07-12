import logging
from flask import (
    make_response,
    Blueprint, 
    request, 
    g, 
)
from flask.json import jsonify

from ..utils import db
from ..utils.decors import *

logger = logging.getLogger(__name__)
bp = Blueprint('rberry', __name__)

@bp.route('/sync')
@must_authenticate
def sync():
    res = db.read_from_table(g.db_conn, 'settings')
    res = [dict(r) for r in res]

    return jsonify(result=res)

@bp.route('/sync', methods=['POST'])
@must_authenticate
@json_required
@check_bad_format
def bot_sync():
    setting_cols = request.get_json()['setting_cols']
    conditions = request.get_json()['conditions']
    res = db.update_table(g.db_conn, 'settings', setting_cols, conditions)
    if res:
        return jsonify(result='success')
    else:
        logger.error(f"Can't sync with bot! data: {setting_cols}  conditions: {conditions}")
        return '', 500