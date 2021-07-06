import random

status_code = lambda resp : int(resp.status.split()[0])

class Test_Login:

    def test_login(self, user, client):
        resp = client.post('/login', data=dict(
            username='wrong',
            password='wrong'
        ))

        assert status_code(resp) == 401
        assert resp.data == b'Username is wrong!\n'

        resp = client.post('/login', data=dict(
            username='wrong',
            password=user['password']
        ))

        assert status_code(resp) == 401
        assert resp.data == b'Username is wrong!\n'

        resp = client.post('/login', data=dict(
            username=user['username'],
            password='wrong'
        ))

        assert status_code(resp) == 401
        assert resp.data == b'Password is wrong!\n'

        resp = client.post('/login', data=dict(
            username=user['username'],
            password=user['password']
        ))

        assert status_code(resp) == 200
        assert resp.is_json == True

        resp_json = resp.get_json()
        assert 'username' in resp_json and 'token' in resp_json
        assert resp_json['username'] == user['username']


class Test_Table_Get_WOC: # WOC = without condition

    def test_table_get(self, client, user, tables):
        for i in range(len(tables)):
            tbl_name = list(tables.keys())[i]
            tbl_rows = tables[tbl_name]['rows']
            tbl_cols = tuple(tbl_rows[0].keys())

            url = f'/db/read/{tbl_name}'
            resp = client.get(
                url,
                headers=[
                    ['X-API-KEY', user['api_key']], 
                ]
            )

            assert status_code(resp) == 200

            result = resp.get_json()['result']

            assert len(result) == len(tbl_rows)
            
            for i in range(len(result)):
                res_cols = list(result[i].keys())

                assert sorted(res_cols) == sorted(tbl_cols) # beacuse res_cols is unosrted sometimes

                res_vals = tuple(result[i][col] for col in tbl_cols)

                assert res_vals == tuple(tbl_rows[i].values())

            # with limit
            data = {'limit': 1}
            resp = client.post(
                url,
                headers=[
                    ['X-API-KEY', user['api_key']], 
                ],
                json=data
            )

            assert status_code(resp) == 200

            result = resp.get_json()['result']

            assert len(result) == 1
            
            res_cols = list(result[0].keys())

            assert sorted(res_cols) == sorted(tbl_cols) # beacuse res_cols is unosrted sometimes

            res_vals = tuple(result[0][col] for col in tbl_cols)

            assert res_vals == tuple(tbl_rows[0].values())


class Test_Table_Get_WC: # WC = With condition

    def test_table_get(self, client, user, tables):
        for i in range(len(tables)):
            tbl_name = list(tables.keys())[i]
            tbl_rows = tables[tbl_name]['rows']
            tbl_cols = tuple(tbl_rows[0].keys())
            tbl_condis = tables[tbl_name]['condis']

            # case1: one condition 
            rand_i = random.randrange(0, len(tbl_condis))
            condi_col = list(tbl_condis.keys())[rand_i]
            condi_val = tbl_condis[condi_col]

            url = f'/db/read/{tbl_name}'

            data = {'conditions': {condi_col: condi_val}}
            resp = client.post(
                url,
                headers=[
                    ['X-API-KEY', user['api_key']], 
                ],
                json=data
            )

            assert status_code(resp) == 200

            result = resp.get_json()['result']

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
            data.update({'limit': 1})
            resp = client.post(
                url,
                headers=[
                    ['X-API-KEY', user['api_key']], 
                ],
                json=data
            )

            assert status_code(resp) == 200

            result = resp.get_json()['result']

            assert len(result) == 1

            res_cols = list(result[0].keys())

            assert sorted(res_cols) == sorted(tbl_cols) # beacuse res_cols is unosrted sometimes

            res_vals = tuple(result[0][col] for col in tbl_cols)

            assert res_vals == tuple(tbl_rows[0].values())


            # case2: multiple conditions
            data = {'conditions': tbl_condis}
            resp = client.post(
                url,
                headers=[
                    ['X-API-KEY', user['api_key']], 
                ],
                json=data
            )

            assert status_code(resp) == 200

            result = resp.get_json()['result']
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
            data.update({'limit': 1})
            resp = client.post(
                url,
                headers=[
                    ['X-API-KEY', user['api_key']], 
                ],
                json=data
            )

            assert status_code(resp) == 200

            result = resp.get_json()['result']

            assert len(result) == 1

            res_cols = list(result[0].keys())

            assert sorted(res_cols) == sorted(tbl_cols) # beacuse res_cols is unosrted sometimes

            res_vals = tuple(result[0][col] for col in tbl_cols)

            assert res_vals == tuple(tbl_rows[0].values())


class Test_Table_Post:

    def test_table_insert(self, client, user, tables):
        for i in range(len(tables)):
            tbl_name = list(tables.keys())[i]
            tbl_rows = tables[tbl_name]['rows']
            tbl_cols = tuple(tbl_rows[0].keys())

            new_vals = {}
            for j in range(len(tbl_cols)):
                col = tbl_cols[j]
                val = tbl_rows[-1][col]

                if type(val) == str:
                    new_val = f'{col}_new'
                elif type(val) == int:
                    new_val = val+1
                else:
                    new_val = None
                    
                new_vals[col] = new_val

            data = {
                'cols': list(new_vals.keys()), 
                'vals': list(new_vals.values())
            }
            resp = client.post(
                f'/db/insert/{tbl_name}', 
                headers=[
                    ['X-API-KEY', user['api_key']], 
                ],
                json=data
            )

            assert status_code(resp) == 200
            assert resp.data == b'Success\n'

            url = f'/db/read/{tbl_name}'
            last_id = new_vals['id']
            data = {'conditions': {'id': last_id}}
            resp = client.post( # we tested table_get before, so it's fine to do this
                url,
                headers=[
                    ['X-API-KEY', user['api_key']], 
                ],
                json=data
            )
            
            result = resp.get_json()['result']
            res_cols = tuple(result[0].keys())

            new_vals_cols = tuple(new_vals.keys())
            new_vals_vals = tuple(new_vals.values())

            assert sorted(res_cols) == sorted(new_vals_cols) # beacuse res_cols is unosrted sometimes

            res_vals = tuple(result[0][col] for col in tbl_cols)

            assert res_vals == new_vals_vals

class Test_Errors:

    def test_db_errors(self, client, user):
        # case 1: right table, without api key, without json for post (providing json doesn't matter)
        a_status = 401
        a_msg = b'Please provide api key with "X-API-KEY" header, Or get a new api key by logging in (/login).\n'

        resp = client.get(
            '/db/read/reports',
        )

        assert status_code(resp) == a_status
        assert resp.data == a_msg

        resp = client.post(
            '/db/read/reports',
        )

        assert status_code(resp) == a_status
        assert resp.data == a_msg

        resp = client.post(
            '/db/insert/reports',
        )

        assert status_code(resp) == a_status
        assert resp.data == a_msg


        # case 2: right table, wrong api key, without json for post (providing json doesn't matter)
        a_status = 401
        a_msg = b'Wrong api key! If you forget your api key you can get a new one by logging in (/login).\n'

        resp = client.get(
            '/db/read/reports',
            headers=[
                ['X-API-KEY', 'wrong_api_key'], 
            ],
        )

        assert status_code(resp) == a_status
        assert resp.data == a_msg

        resp = client.post(
            '/db/read/reports',
            headers=[
                ['X-API-KEY', 'wrong_api_key'], 
            ],
        )

        assert status_code(resp) == a_status
        assert resp.data == a_msg

        resp = client.post(
            '/db/insert/reports',
            headers=[
                ['X-API-KEY', 'wrong_api_key'], 
            ],
        )

        assert status_code(resp) == a_status
        assert resp.data == a_msg


        # case 3: right table, right api key, no json for post
        a_status = 415
        a_msg = b'Please provide the JSON too!\n'

        resp = client.post(
            '/db/read/reports',
            headers=[
                ['X-API-KEY', user['api_key']], 
            ],
        )

        assert status_code(resp) == a_status
        assert resp.data == a_msg

        resp = client.post(
            '/db/read/reports',
            headers=[
                ['X-API-KEY', user['api_key']], 
            ],
        )

        assert status_code(resp) == a_status
        assert resp.data == a_msg
        

        # case 4: wrong table, right api key, json for post
        a_status = 422
        a_msg = b'Provided table name is wrong!\n'

        resp = client.get(
            '/db/read/wrong_table',
            headers=[
                ['X-API-KEY', user['api_key']], 
            ],
        )

        assert status_code(resp) == a_status
        assert resp.data == a_msg

        resp = client.post(
            '/db/read/wrong_table',
            headers=[
                ['X-API-KEY', user['api_key']], 
            ],
            json={'limit': 1}
        )

        assert status_code(resp) == a_status
        assert resp.data == a_msg

        resp = client.post(
            '/db/insert/wrong_table',
            headers=[
                ['X-API-KEY', user['api_key']], 
            ],
            json={'limit': 1}
        )

        assert status_code(resp) == a_status
        assert resp.data == a_msg

    def test_login_errors(self, client, user):
        a_status = 401
        a_msg = b'Please provide your Username!\nPlease provide your Password!\n'

        resp = client.post(
            '/login',
        )
        
        assert status_code(resp) == a_status
        assert resp.data == a_msg

        
        a_msg = b'Please provide your Password!\n'
        resp = client.post(
            '/login',
            data={
                'username': user['username']
            }
        )
        
        assert status_code(resp) == a_status
        assert resp.data == a_msg

        
        a_msg = b'Please provide your Username!\n'
        resp = client.post(
            '/login',
            data={
                'password': user['password']
            }
        )
        
        assert status_code(resp) == a_status
        assert resp.data == a_msg

        
        a_msg = b'Username is wrong!\n'
        resp = client.post(
            '/login',
            data={
                'username': 'wrong_username',
                'password': user['password']
            }
        )
        
        assert status_code(resp) == a_status
        assert resp.data == a_msg

        
        a_msg = b'Password is wrong!\n'
        resp = client.post(
            '/login',
            data={
                'username': user['username'],
                'password': 'wrong_password'
            }
        )
        
        assert status_code(resp) == a_status
        assert resp.data == a_msg