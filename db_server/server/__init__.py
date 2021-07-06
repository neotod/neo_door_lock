from .parts import blueprints
from .parts.utils.db import set_db_conn, close_db, init_db
from .config import Testing

from flask import Flask

app = Flask(__name__)
app.config.from_object(Testing)

app.before_first_request(init_db)
app.before_request(set_db_conn)
app.teardown_appcontext(close_db)

@app.route('/')
def index():
    msg = '''
    URLs:
        /db/read/<table_name> : method=GET
        /db/read/<table_name> : method=POST : data=JSON : JSON={conditions | limit}

        /db/insert/<table_name> : method=POST : data=JSON : JSON={cols, vals}

        /login : method=POST : data=form : form={username, password}
    '''
    return msg

app.register_blueprint(blueprints.db.bp)
app.register_blueprint(blueprints.login.bp)


import logging
# logging.basicConfig(filename=app.config['LOGS_PATH'], format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)