import time
from requests import post

from .exceptions import ServerUnreachable

URLs = {
    'read': 'https://dbs-neotod.fandogh.cloud/db/read',
    'insert': 'https://dbs-neotod.fandogh.cloud/db/insert',
    'update': 'https://dbs-neotod.fandogh.cloud/db/update',
    'delete': 'https://dbs-neotod.fandogh.cloud/db/delete',

    'login': 'https://dbs-neotod.fandogh.cloud/login'
}
MAX_ATTEMPTS = 3

credentials = {'username': '', 'password': '', 'api_key': ''}

def update_credentials(username, password):
    global credentials

    credentials['username'] = username
    credentials['password'] = password

    attempts = MAX_ATTEMPTS
    while True:
        resp = post(URLs['login'], data={'username': username, 'password': password})
        if resp.status_code == 200:
            credentials['api_key'] = resp.json()['token']
            break

        if attempts == 0:
            raise ServerUnreachable("Can't connect to db server to get the api key!", URLs['login'])

        attempts -= 1
        time.sleep(0.7)

def send_request(url, json):
    attempts = MAX_ATTEMPTS
    headers = {'X-API-KEY': credentials['api_key']}
    while True:
        resp = post(url, json=json, headers=headers)

        if resp.status_code == 200:
            return resp.json()
        elif resp.status_code == 401:
            update_credentials(credentials['username'], credentials['password'])
            headers['X-API-KEY'] = credentials['api_key']
            continue
            
        attempts -= 1
        time.sleep(0.5)
        if attempts == 0:
            break

    return 'failed'