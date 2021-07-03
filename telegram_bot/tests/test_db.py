import os
import random
import sqlite3
import unittest
from parts.db.utils import *
from sqlite3 import Connection

class Test_DB(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.test_db_path = os.path.join('datas', 'test_db.db')
        cls.sql_path = os.path.join('datas', 'init_db.sql')

        cls.tables = ['pass_hashes', 'users', 'events', 'reports']

        cls.tables_cols = [
            ('hash', 'len'),
            ('name_', 'lastname', 'username', 'pass_hash_id', 'email'),
            ('name_', 'text_'),
            ('event_id', 'date', 'time', 'more_info'),
        ]

        cls.conn = init_db(cls.test_db_path, cls.sql_path)

    @classmethod
    def tearDownClass(cls) -> None:
        os.remove(cls.test_db_path)
        cls.conn.close()

    def test_insert_into_table(self):
        tables_vals = (
            (
                ('pass_hash', 'pass_len_hash'),
                ('neotod', 'فامیل', 'neotod1', 2, 'neotod1@gmail.com'),
                ('event', 'متن'),
                (1, 'more_info', 'date', 'time')
            ),
            (
                (
                    ('pass_hash1', 'pass_len_hash1'), 
                    ('pass_hash2', 'pass_len_hash2'), 
                    ('pass_hash3', 'pass_len_hash3')
                ),
                (
                    ('neotod', 'neotod', 'neotod2', 3, 'neotod2@gmail.com'),
                    ('اسم', 'lastname2', 'neotod3', 4, 'hey@protonmail.com')
                ),
                (
                    ('event', 'متن'),
                    ('event1', 'متن1'),
                    ('event2', 'متن2'),
                    ('event3', 'متن3'),
                ),
                (
                    (1, 'more_info', 'date', 'time'),
                    (2, 'more_info2', 'date2', 'time2'),
                )
            ),
        )

        for i in range(len(tables_vals)):
            for j in range(len(self.tables)):
                tbl_name = self.tables[j]
                tbl_cols = self.tables_cols[j]
                tbl_vals = tables_vals[i][j]

                with self.subTest():
                    self.assertTrue(insert_into_table(self.conn, tbl_name, tbl_cols, tbl_vals))

    def test_read_from_table(self):
        with self.subTest():
            for i in range(len(self.tables)):
                tbl_name = self.tables[i]
                tbl_cols = self.tables_cols[i]
                
                self.assertNotEqual(read_from_table(self.conn, tbl_name), [])
                for col in tbl_cols:
                    self.assertNotEqual(read_from_table(self.conn, tbl_name, col), [])
                self.assertNotEqual(read_from_table(self.conn, tbl_name, tbl_cols), [])

        conditions = (
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
                'id': 1,
                'name_': 'lock_state_change'
            },
            {
                'event_id': ('in', (2, 3)),
                'date': ('between', ('1400-02-01', '1400-04-30'))
            }
        )

        with self.subTest():
            for i in range(len(self.tables)):
                tbl_name = self.tables[i]
                tbl_cols = self.tables_cols[i]
                tbl_condis = conditions[i]

                rand_num = random.randrange(0, len(tbl_condis))
                condis_keys = list(tbl_condis.keys())
                choosed_condis = {key: tbl_condis[key] for key in condis_keys[:rand_num+1]} # selecting some conditions from table's declared conditions (conditions tuple above)

                self.assertNotEqual(read_from_table(self.conn, tbl_name, None, choosed_condis), [])
                for col in tbl_cols:
                    self.assertNotEqual(read_from_table(self.conn, tbl_name, col, choosed_condis), [])
                self.assertNotEqual(read_from_table(self.conn, tbl_name, tbl_cols, choosed_condis), [])

    def test_update_table(self):
        settings_vals = (
                ('pass_hash_new', 'pass_len_hash_new'),
                ('neotod_new', 'فامیل جدید', 'neotod_new', 1, 'neotod@gmail.com_new'),
                ('event_new', 'متن جدید'),
                (3, 'more_info_new', 'date_new', 'time_new')
        )

        # case 1: updating one random column + updating every column | without condition
        with self.subTest():
            for i in range(len(self.tables)):
                tbl_name = self.tables[i]
                tbl_cols = list(self.tables_cols[i])
                tbl_vals = list(settings_vals[i])

                rand_i = random.randrange(0, len(tbl_cols))
                rand_col = tbl_cols[rand_i]
                rand_val = tbl_vals[rand_i]

                settings_cols = {rand_col: rand_val}
                self.assertTrue(update_table(self.conn, tbl_name, settings_cols))

                self.__class__.tearDownClass()
                self.__class__.conn = init_db(self.__class__.test_db_path, self.__class__.sql_path)

                settings_cols = {tbl_cols[j]: tbl_vals[j] for j in range(len(tbl_cols))}
                self.assertTrue(update_table(self.conn, tbl_name, settings_cols))

        self.__class__.tearDownClass()
        self.__class__.conn = init_db(self.__class__.test_db_path, self.__class__.sql_path)

        # case 2: updating one random column + updating every column | with condition
        conditions = (
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
                'id': 1,
                'name_': 'lock_state_change'
            },
            {
                'event_id': ('in', (2, 3)),
                'date': ('between', ('1400-02-01', '1400-04-30'))
            }
        )

        with self.subTest():
            for i in range(len(self.tables)):
                tbl_name = self.tables[i]
                tbl_cols = list(self.tables_cols[i])
                tbl_vals = list(settings_vals[i])
                tbl_condis = conditions[i]

                rand_i = random.randrange(0, len(tbl_cols))
                rand_col = tbl_cols[rand_i]
                rand_val = tbl_vals[rand_i]

                rand_num = random.randrange(0, len(tbl_condis))
                condis_keys = list(tbl_condis.keys())
                choosed_condis = {key: tbl_condis[key] for key in condis_keys[:rand_num+1]} # selecting some conditions from table's declared conditions (conditions tuple above)

                settings_cols = {rand_col: rand_val}
                self.assertTrue(update_table(self.conn, tbl_name, settings_cols, choosed_condis))
                
                self.__class__.tearDownClass()
                self.__class__.conn = init_db(self.__class__.test_db_path, self.__class__.sql_path)

                settings_cols = {tbl_cols[j]: tbl_vals[j] for j in range(len(tbl_cols))}
                self.assertTrue(update_table(self.conn, tbl_name, settings_cols, choosed_condis))

    def test_get_table_columns(self):
        for i in range(len(self.tables)):
            tbl_name = self.tables[i]
            tbl_cols = self.tables_cols[i]

            res = list(get_table_columns(self.conn, tbl_name))
            res.remove('id')
            res = tuple(res)
            self.assertEqual(res, tbl_cols)