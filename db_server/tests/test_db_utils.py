import random
from types import new_class

from .test_utils.db import get_new_vals
from server.parts.utils import db


class Test_DB:
    
    def test_insert_into_table(self, db_conn, tables):
        for i in range(len(tables)):
            tbl_name = list(tables.keys())[i]
            tbl_rows = tables[tbl_name]['rows']
            tbl_cols = tuple(tbl_rows[0].keys())

            new_vals = get_new_vals(list(tbl_rows[-1].values()))
            
            assert db.insert_into_table(db_conn, tbl_name, tbl_cols, new_vals) == True

            multiple_new_vals = []
            rand_num = random.randrange(1, 5)
            for _ in range(rand_num):
                new_vals = get_new_vals(new_vals)
                multiple_new_vals.append(new_vals)

            assert db.insert_into_table(db_conn, tbl_name, tbl_cols, multiple_new_vals) == True # multiple list of values

    def test_read_from_table(self, db_conn, tables):
        for i in range(len(tables)):
            tbl_name = list(tables.keys())[i]
            tbl_rows = tables[tbl_name]['rows']
            tbl_cols = tuple(tbl_rows[0].keys())

            assert db.read_from_table(db_conn, tbl_name) != []

            for col in tbl_cols:
                assert db.read_from_table(db_conn, tbl_name, col) != []
            
            assert db.read_from_table(db_conn, tbl_name, tbl_cols) != []

        for i in range(len(tables)):
            tbl_name = list(tables.keys())[i]
            tbl_rows = tables[tbl_name]['rows']
            tbl_cols = tuple(tbl_rows[0].keys())
            tbl_condis = tables[tbl_name]['condis']

            rand_num = random.randrange(0, len(tbl_condis))
            condis_keys = list(tbl_condis.keys())
            choosed_condis = {key: tbl_condis[key] for key in condis_keys[:rand_num+1]} # selecting some conditions from table's declared conditions (conditions tuple above)

            assert db.read_from_table(db_conn, tbl_name, None, choosed_condis) != []
            for col in tbl_cols:
                assert db.read_from_table(db_conn, tbl_name, col, choosed_condis) != []

            assert db.read_from_table(db_conn, tbl_name, tbl_cols, choosed_condis) != []

    def test_update_table(self, db_conn, files_path, tables):
        tbls_new_vals = []
        for i in range(len(tables)):
            tbl_name = list(tables.keys())[i]
            tbl_rows = tables[tbl_name]['rows']
            tbl_cols = tuple(tbl_rows[0].keys())

            new_vals = {}
            for j in range(len(tbl_cols)):
                col = tbl_cols[j]
                val = tbl_rows[-1][col]

                if col == 'id':
                    continue

                if type(val) == str:
                    new_val = f'{col}_new'
                elif type(val) == int:
                    new_val = val+1
                else:
                    new_val = None
                    
                new_vals[col] = new_val

            tbls_new_vals.append(new_vals)


        # case 1: updating one random column + updating every column | without condition
        for i in range(len(tables)):
            tbl_name = list(tables.keys())[i]
            tbl_rows = tables[tbl_name]['rows']
            tbl_cols = tuple(tbl_rows[0].keys())
            settings_vals = tbls_new_vals[i]

            rand_col = random.choice(tuple(settings_vals.keys()))
            rand_val = settings_vals[rand_col]

            settings_cols = {rand_col: rand_val}
            assert db.update_table(db_conn, tbl_name, settings_cols) == True

            db.init_db(files_path['test_db'], files_path['init_sql']) # reseting the db

            settings_cols = {col: val for col, val in settings_vals.items()}
            assert db.update_table(db_conn, tbl_name, settings_cols) == True


        db.init_db(files_path['test_db'], files_path['init_sql'])


        # case 2: updating one random column + updating every column | with condition
        for i in range(len(tables)):
            tbl_name = list(tables.keys())[i]
            tbl_rows = tables[tbl_name]['rows']
            tbl_cols = tuple(tbl_rows[0].keys())
            tbl_condis = tables[tbl_name]['condis']
            settings_vals = tbls_new_vals[i]

            rand_col = random.choice(tuple(settings_vals.keys()))
            rand_val = settings_vals[rand_col]

            rand_num = random.randrange(0, len(tbl_condis))
            condis_cols = list(tbl_condis.keys())
            choosed_condis = {col: tbl_condis[col] for col in condis_cols[:rand_num+1]} # selecting some conditions from table's declared conditions (conditions tuple above)

            settings_cols = {rand_col: rand_val}
            assert db.update_table(db_conn, tbl_name, settings_cols, choosed_condis) == True
            

            db.init_db(files_path['test_db'], files_path['init_sql'])

            settings_cols = {col: val for col, val in settings_vals.items()}
            assert db.update_table(db_conn, tbl_name, settings_cols, choosed_condis) == True

    def test_get_table_columns(self, db_conn, tables):
        for i in range(len(tables)):
            tbl_name = list(tables.keys())[i]
            tbl_rows = tables[tbl_name]['rows']
            tbl_cols = tuple(tbl_rows[0].keys())

            res = list(db.get_table_columns(db_conn, tbl_name))
            res = tuple(res)

            assert res == tbl_cols

    def test_delete_from_table(self, db_conn, files_path, tables):
        for tbl_name in tables:
            condis = tables[tbl_name]['condis']

            rand_col = random.choice(list(condis.keys()))
            rand_condi = {rand_col: condis[rand_col]}

            assert db.delete_from_table(db_conn, tbl_name, rand_condi) == True
            
            db.init_db(files_path['test_db'], files_path['init_sql'])

            assert db.delete_from_table(db_conn, tbl_name, condis) == True