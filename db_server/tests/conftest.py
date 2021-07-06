import os
import pytest

from server.parts.utils import db
from server import app

DEBUG = True

@pytest.fixture(scope='class')
def files_path():
    return {
        'test_db': os.path.join('tests', 'test_datas', 'test_db.db'),
        'init_sql': os.path.join('tests', 'test_datas', 'init_db.sql') 
    }

@pytest.fixture(autouse=True, scope='class')
def make_and_reomve_db(files_path):
    db.init_db(files_path['test_db'], files_path['init_sql'])

    yield

    os.remove(files_path['test_db'])

@pytest.fixture
def db_conn(files_path):
    db.init_db(files_path['test_db'], files_path['init_sql'])
    conn = db.get_db_conn(files_path['test_db'])

    yield conn

    conn.close()

@pytest.fixture
def tables():
    tbls_names = ('events', 'reports', 'pass_hashes', 'users', 'api_tokens')
    tbls_cols = (
        ('id', 'name_', 'text_'),
        ('id', 'event_id', 'date', 'time', 'more_info'),
        ('id', 'hash', 'len'),
        ('id', 'name_', 'lastname', 'username', 'pass_hash_id', 'email'),
        ('id', 'user_id', 'token')
    )
    tbls_condis = ( # conditions
        {
            'id': 1,
            'name_': 'lock_state_change'
        },
        {
            'event_id': ('in', (1, 2, 4)),
            'date': ('between', ('1400-02-01', '1400-04-30')),
        },
        {
            'id': 1,
            'hash': 'd64ddcd5979fd920a8809276b82f419f9994c58e85d54cf842d3b5060212bba2',
        },
        {
            'id': 1,
            'username': 'neotod',
            'pass_hash_id': 1,
            'email': 'neotod@gmail.com'
        },
        {
            'user_id': 1,
            'token': '01aa857beea71a6afb169de2238a20de480c4f8a87967cde5630bade2e4a351b'
        }
    )
    tbls_rows_vals = (
        (
            (1, 'lock_state_change','تغییر وضعیت قفل'),
            (2, 'user_login','ورود کاربر به بات'),
            (3, 'entry','ورود'),
            (4, 'user_change','تغییر کاربر'),
        ),
        (
            (1, 1, '1400-02-10', '10:20:20', 'حالت فعلی: فعال'),
            (2, 1, '1400-02-15', '10:30:01', 'حالت فعلی: غیرفعال'),
            (3, 2, '1400-03-10', '20:02:20', 'username: neotod'),
            (4, 3, '1400-05-20', '11:20:20', 'ورود موفق'),
            (5, 3, '1400-05-01', '15:20:20', 'ورود ناموفق'),
        ),
        (
            (1, 'd64ddcd5979fd920a8809276b82f419f9994c58e85d54cf842d3b5060212bba2','e7f6c011776e8db7cd330b54174fd76f7d0216b612387a5ffcfb81e6f0919683'),
        ),
        (
            (1, 'neotod', None, 'neotod', 1, 'neotod@gmail.com'),
        ),
        (
            (1, 1, '01aa857beea71a6afb169de2238a20de480c4f8a87967cde5630bade2e4a351b'),
        ),
    )

    tbls_rows = []
    for i in range(len(tbls_names)):
        rows = []
        cols = tbls_cols[i]
        rows_vals = tbls_rows_vals[i]

        for vals in rows_vals:
            rows.append(dict(zip(cols, vals)))

        tbls_rows.append(rows)

    if not DEBUG:
        num = len(tbls_names)
    else:
        num = 2

    tables = {}
    for i in range(num):
        rows = tbls_rows[i]
        condis = tbls_condis[i]
            
        tbl_dict = {
            'rows': rows,
            'condis': condis, 
        }

        tables.update(
            { tbls_names[i]: tbl_dict }
        )
        
    return tables

@pytest.fixture
def user():
    return {
        'username': 'neotod',
        'password': 'neotod',
        'api_key': '01aa857beea71a6afb169de2238a20de480c4f8a87967cde5630bade2e4a351b'
    }

@pytest.fixture
def client(files_path):
    with app.test_client() as client_:
        yield client_
    
    db.init_db(files_path['test_db'], files_path['init_sql']) # reset the db for next use
