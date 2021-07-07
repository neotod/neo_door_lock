import os

class Base:
    SECRET_KEY = os.urandom(32)
    JSON_AS_ASCII = False
    INIT_SQL_PATH =  os.path.join('datas', 'init_db.sql')
    DB_PATH = os.path.join('datas', 'tiny_db.db')
    LOGS_PATH = os.path.join('datas', 'log.log')
    FORBIDDEN_TABLES = ['api_tokens']

class Development(Base):
    ENV = 'development'

class Testing(Development):
    INIT_SQL_PATH =  os.path.join('tests', 'test_datas', 'init_db.sql')
    DB_PATH = os.path.join('tests', 'test_datas', 'test_db.db')
    TESTING = True

class Production(Base):
    ENV = 'production'


formats = {}
formats.update({
'db-read':
'''
safety: safe
data: json
format:
    {
        table_name1: {
                conditions: dict, limit: int
        },
        table_name2: {
                conditions: dict, limit: int
        },
        .
        .
        .
    }
info:
    conditions are optional, it can be just table_name: []
    limit is optional, default limit is 50 rows
'''
})

formats.update({
'db-insert':
'''
safety: NOT-SAFE
data: json
format:
    {
        table_name1: {
                cols: list, vals: list | list[list,...]
        },
        table_name2: {
                cols: list, vals: list | list[list,...]
        },
        .
        .
        .
    }
info:
    cols length and vals length must be equal
'''
})

formats.update({
'db-update':
'''
safety: NOT-SAFE
data: json
format:
    {
        table_name1: [
                { setting_cols: dict, conditions: dict },
                ...
        ],
        table_name2: [
                { setting_cols: dict, conditions: dict },
                ...
        ],
        .
        .
        .
    }
info:
    conditions are optional, if you omit them, then the whole table will be updated
'''
})

formats.update({
'db-delete':
'''
safety: NOT-SAFE
data: json
format:
    {
        table_name1: [
                condition1:dict, condition2:dict, ...
        ],
        table_name2: [
                condition1:dict, condition2:dict, ...
        ],
        .
        .
        .
    }
info:
    conditions are not optional! (do you like to delete your whole table?)
    each conditons is related to a series of rows that wil get deleted
''',
})

formats.update({
'login':
'''
data: form
format: 
        username = your_username 
        password = your_password 
'''
})
