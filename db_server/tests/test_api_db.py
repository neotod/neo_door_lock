import random
from .test_utils.db import get_new_vals

status_code = lambda resp : int(resp.status.split()[0])

class Test_Table_Read:
    def test_without_condi(self, client, user, tables, urls):
        for i in range(len(tables)):
            tbl_name = list(tables.keys())[i]
            tbl_rows = tables[tbl_name]['rows']
            tbl_cols = tuple(tbl_rows[0].keys())

            data = {tbl_name: {}}
            resp = client.post(
                urls['db-read'],
                headers=[
                    ['X-API-KEY', user['api_key']], 
                ],
                json=data
            )

            assert status_code(resp) == 200

            result = resp.get_json()['result'][tbl_name]

            assert len(result) == len(tbl_rows)
            
            for i in range(len(result)):
                res_cols = list(result[i].keys())

                assert sorted(res_cols) == sorted(tbl_cols) # beacuse res_cols is unosrted sometimes

                res_vals = tuple(result[i][col] for col in tbl_cols) # beacuse res_vals is unosrted sometimes

                assert res_vals == tuple(tbl_rows[i].values())

            # with limit
            data[tbl_name].update({'limit': 1})
            resp = client.post(
                urls['db-read'],
                headers=[
                    ['X-API-KEY', user['api_key']], 
                ],
                json=data
            )

            assert status_code(resp) == 200

            result = resp.get_json()['result'][tbl_name]

            assert len(result) == 1
            
            res_cols = list(result[0].keys())

            assert sorted(res_cols) == sorted(tbl_cols) # beacuse res_cols is unosrted sometimes

            res_vals = tuple(result[0][col] for col in tbl_cols)

            assert res_vals == tuple(tbl_rows[0].values())


        # test multiple tables
        rand_num = random.randrange(2, len(tables)+1)
        rand_tbls = random.sample(list(tables.keys()), k=rand_num)
        data = {tbl: {} for tbl in rand_tbls}
        resp = client.post(
                urls['db-read'],
                headers=[
                    ['X-API-KEY', user['api_key']], 
                ],
                json=data
        )

        assert status_code(resp) == 200

        result = resp.get_json()['result']
        for tbl_name in rand_tbls:
            assert tbl_name in result
            
            tbl_res = result[tbl_name]
            tbl_rows = tables[tbl_name]['rows']
            tbl_cols = tuple(tbl_rows[0].keys())

            assert len(tbl_res) == len(tbl_rows)
            
            for i in range(len(tbl_res)):
                res_cols = list(tbl_res[i].keys())

                assert sorted(res_cols) == sorted(tbl_cols) # beacuse res_cols is unosrted sometimes

                res_vals = tuple(tbl_res[i][col] for col in tbl_cols) # beacuse res_vals is unosrted sometimes

                assert res_vals == tuple(tbl_rows[i].values())

    def test_with_condi(self, client, user, tables, urls):
        for i in range(len(tables)):
            tbl_name = list(tables.keys())[i]
            tbl_rows = tables[tbl_name]['rows']
            tbl_cols = tuple(tbl_rows[0].keys())
            tbl_condis = tables[tbl_name]['condis']

            # case1: one condition 
            rand_i = random.randrange(0, len(tbl_condis))
            condi_col = list(tbl_condis.keys())[rand_i]
            condi_val = tbl_condis[condi_col]

            data = {tbl_name: {}}
            data[tbl_name].update({
                'conditions': {condi_col: condi_val}
            })
            resp = client.post(
                urls['db-read'],
                headers=[
                    ['X-API-KEY', user['api_key']], 
                ],
                json=data
            )

            assert status_code(resp) == 200

            result = resp.get_json()['result'][tbl_name]

            if tbl_name != 'reports':
                assert len(result) == 1
            else:
                assert len(result) == 3

            for i in range(len(result)):
                res_cols = list(result[i].keys())

                assert sorted(res_cols) == sorted(tbl_cols) # beacuse res_cols is unosrted sometimes

                res_vals = tuple(result[i][col] for col in tbl_cols)

                assert res_vals == tuple(tbl_rows[i].values())


            # with limit
            data[tbl_name].update({'limit': 1})
            resp = client.post(
                urls['db-read'],
                headers=[
                    ['X-API-KEY', user['api_key']], 
                ],
                json=data
            )

            assert status_code(resp) == 200

            result = resp.get_json()['result'][tbl_name]

            assert len(result) == 1

            res_cols = list(result[0].keys())

            assert sorted(res_cols) == sorted(tbl_cols) # beacuse res_cols is unosrted sometimes

            res_vals = tuple(result[0][col] for col in tbl_cols)

            assert res_vals == tuple(tbl_rows[0].values())


            # case2: multiple conditions
            data[tbl_name] = {'conditions': tbl_condis}
            resp = client.post(
                urls['db-read'],
                headers=[
                    ['X-API-KEY', user['api_key']], 
                ],
                json=data
            )

            assert status_code(resp) == 200

            result = resp.get_json()['result'][tbl_name]
            if tbl_name != 'reports':
                assert len(result) == 1
            else:
                assert len(result) == 3

            for i in range(len(result)):
                res_cols = list(result[i].keys())

                assert sorted(res_cols) == sorted(tbl_cols) # beacuse res_cols is unosrted sometimes

                res_vals = tuple(result[i][col] for col in tbl_cols)

                assert res_vals == tuple(tbl_rows[i].values())


            # with limit
            data[tbl_name].update({'limit': 1})
            resp = client.post(
                urls['db-read'],
                headers=[
                    ['X-API-KEY', user['api_key']], 
                ],
                json=data
            )

            assert status_code(resp) == 200

            result = resp.get_json()['result'][tbl_name]

            assert len(result) == 1

            res_cols = list(result[0].keys())

            assert sorted(res_cols) == sorted(tbl_cols) # beacuse res_cols is unosrted sometimes

            res_vals = tuple(result[0][col] for col in tbl_cols)

            assert res_vals == tuple(tbl_rows[0].values())


        # test multiple tables
        rand_num = random.randrange(2, len(tables)+1)
        rand_tbls = random.sample(list(tables.keys()), k=rand_num)
        data = {tbl: {'conditions': tables[tbl]['condis']} for tbl in rand_tbls}
        resp = client.post(
                urls['db-read'],
                headers=[
                    ['X-API-KEY', user['api_key']], 
                ],
                json=data
        )

        assert status_code(resp) == 200

        result = resp.get_json()['result']
        for tbl_name in rand_tbls:
            assert tbl_name in result
            
            tbl_res = result[tbl_name]
            tbl_rows = tables[tbl_name]['rows']
            tbl_cols = tuple(tbl_rows[0].keys())

            if tbl_name != 'reports':
                assert len(tbl_res) == 1
            else:
                assert len(tbl_res) == 3
            
            for i in range(len(tbl_res)):
                res_cols = list(tbl_res[i].keys())

                assert sorted(res_cols) == sorted(tbl_cols) # beacuse res_cols is unosrted sometimes

                res_vals = tuple(tbl_res[i][col] for col in tbl_cols) # beacuse res_vals is unosrted sometimes

                assert res_vals == tuple(tbl_rows[i].values())

class Test_Table_Insert:
    def test_without_condi(self, client, user, tables, urls):
        saved = {} # will using them afterward

        for i in range(len(tables)):
            tbl_name = list(tables.keys())[i]
            tbl_rows = tables[tbl_name]['rows']
            tbl_cols = tuple(tbl_rows[0].keys())
            saved[tbl_name] = {}

            new_vals = get_new_vals(list(tbl_rows[-1].values()))

            saved[tbl_name]['cols'] = tbl_cols
            saved[tbl_name]['vals'] = new_vals

            data = {tbl_name: {}}
            data[tbl_name] = {
                'cols': tbl_cols, 
                'vals': new_vals
            }
            resp = client.post(
                urls['db-insert'],
                headers=[
                    ['X-API-KEY', user['api_key']], 
                ],
                json=data
            )

            assert status_code(resp) == 200
            result = resp.get_json()['result'][tbl_name]
            assert result == 'success'
            
            last_id = new_vals[0]
            data[tbl_name] = {'conditions': {'id': last_id}}
            resp = client.post( # we tested table_get before, so it's fine to do this
                urls['db-read'],
                headers=[
                    ['X-API-KEY', user['api_key']], 
                ],
                json=data
            )
            
            result = resp.get_json()['result'][tbl_name]
            res_cols = tuple(result[0].keys())

            assert sorted(res_cols) == sorted(tbl_cols) # beacuse res_cols is unosrted sometimes

            res_vals = tuple(result[0][col] for col in tbl_cols)

            assert res_vals == tuple(new_vals)

        
        # test multiple tables
        for tbl_name in tables:
            prev_vals = saved[tbl_name]['vals']
            saved[tbl_name]['vals'] = get_new_vals(prev_vals)

        rand_num = random.randrange(2, len(tables)+1)
        rand_tbls = random.sample(list(tables.keys()), k=rand_num)
        data = {
            tbl: {
                'cols': saved[tbl]['cols'], 
                'vals': saved[tbl]['vals']
            } for tbl in rand_tbls
        }
        resp = client.post(
                urls['db-insert'],
                headers=[
                    ['X-API-KEY', user['api_key']], 
                ],
                json=data
        )

        assert status_code(resp) == 200

        result = resp.get_json()['result']
        for tbl_name in rand_tbls:
            assert tbl_name in result
            assert result[tbl_name] == 'success'

class Test_Errors:

    def test_db_errors(self, client, user, urls):
        # case 1: no api key, no json for post (providing json doesn't matter)
        a_status = 401
        a_msg = b'Please provide api key with "X-API-KEY" header, Or get a new api key by logging in (/login).\n'

        resp = client.post(
            urls['db-read'],
        )

        assert status_code(resp) == a_status
        assert resp.data == a_msg

        resp = client.post(
            urls['db-insert'],
        )

        assert status_code(resp) == a_status
        assert resp.data == a_msg


        # case 2: wrong api key, without json for post (providing json doesn't matter)
        a_status = 401
        a_msg = b'Wrong api key! If you forget your api key you can get a new one by logging in (/login).\n'

        resp = client.post(
            urls['db-read'],
            headers=[
                ['X-API-KEY', 'wrong_api_key'], 
            ],
        )

        assert status_code(resp) == a_status
        assert resp.data == a_msg

        resp = client.post(
            urls['db-insert'],
            headers=[
                ['X-API-KEY', 'wrong_api_key'], 
            ],
        )

        assert status_code(resp) == a_status
        assert resp.data == a_msg


        # case 3: right api key, no json for post
        a_status = 415
        a_msg = b'Please provide the JSON too!\n'

        resp = client.post(
            urls['db-read'],
            headers=[
                ['X-API-KEY', user['api_key']], 
            ],
        )

        assert status_code(resp) == a_status
        assert resp.data == a_msg

        resp = client.post(
            urls['db-insert'],
            headers=[
                ['X-API-KEY', user['api_key']], 
            ],
        )

        assert status_code(resp) == a_status
        assert resp.data == a_msg