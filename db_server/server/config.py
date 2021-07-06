import os

class Base:
    SECRET_KEY = os.urandom(32)
    JSON_AS_ASCII = False
    INIT_SQL_PATH =  os.path.join('datas', 'init_db.sql')
    DB_PATH = os.path.join('datas', 'tiny_db.db')

class Development(Base):
    ENV = 'development'

class Testing(Development):
    INIT_SQL_PATH =  os.path.join('tests', 'test_datas', 'init_db.sql')
    DB_PATH = os.path.join('tests', 'test_datas', 'test_db.db')
    TESTING = True

class Production(Base):
    ENV = 'production'