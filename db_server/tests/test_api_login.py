status_code = lambda resp : int(resp.status.split()[0])

class Test_Login:

    def test_login(self, user, client):
        resp = client.post('/login', data=dict(
            username=user['username'],
            password=user['password']
        ))

        assert status_code(resp) == 200
        assert resp.is_json == True

        resp_json = resp.get_json()
        assert 'username' in resp_json and 'token' in resp_json
        assert resp_json['username'] == user['username']

class Test_Errors:

    def test_login_errors(self, client, user):
        a_status = 422
        a_msg = b'Please use the correct format for your JSON.\n For getting correct formats go to /format/login.\n'

        resp = client.post(
            '/login',
        )
        
        assert status_code(resp) == a_status
        assert resp.data == a_msg

        
        resp = client.post(
            '/login',
            data={
                'username': user['username']
            }
        )
        
        assert status_code(resp) == a_status
        assert resp.data == a_msg

        
        resp = client.post(
            '/login',
            data={
                'password': user['password']
            }
        )
        
        assert status_code(resp) == a_status
        assert resp.data == a_msg

        a_status = 401
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