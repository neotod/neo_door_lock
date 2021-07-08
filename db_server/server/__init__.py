from .config import Production, formats
from .parts import blueprints
from .parts.utils.db import set_db_conn, close_db, init_db
from .parts.utils.decors import log

from flask import Flask, make_response

app = Flask(__name__)
app.config.from_object(Production)

app.before_first_request(init_db)
app.before_request(set_db_conn)
app.teardown_appcontext(close_db)


@app.route('/')
def index():
    msg = '''
    URLs:
        /db/read   : method=POST : data=JSON
        /db/insert : method=POST : data=JSON
        /db/update : method=POST : data=JSON
        /db/delete : method=POST : data=JSON

        /login : method=POST : data=form

        goto /format/<url_prefix> for more info about data
    '''
    return msg

@app.route('/format/<url_prefix>')
@log
def data_formats(url_prefix):
    try:
        msg = formats[url_prefix]
    except KeyError:
        msg = f'Choose from these: \n{list(formats.keys())}'

    return make_response(msg)


app.register_blueprint(blueprints.db.bp)
app.register_blueprint(blueprints.login.bp)


import logging
if app.config['TESTING']:
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
else:
    logging.basicConfig(filename=app.config['LOGS_PATH'], format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)