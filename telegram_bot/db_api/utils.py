import time
import logging
from requests import get, post

from .exceptions import *

URL_MAIN = 'https://dbs-micro1400.fandogh.cloud'
URLs = {
    'db': {
        'read':   f'{URL_MAIN}/db/read',
        'insert': f'{URL_MAIN}/db/insert',
        'update': f'{URL_MAIN}/db/update',
        'delete': f'{URL_MAIN}/db/delete',
        'backup': f'{URL_MAIN}/db/backup'
    },
    'sync' : f'{URL_MAIN}/sync',
    'login': f'{URL_MAIN}/login'
}
MAX_ATTEMPTS = 3

credentials = {'username': '', 'password': '', 'api_key': ''}
logger = logging.getLogger(__name__)

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
            raise ServerUnreachable("Can't connect to db server to get the api key! (maybe username and password are wrong)", URLs['login'])

        attempts -= 1
        time.sleep(0.7)

def send_req(url, method, **kwargs):
    attempts = MAX_ATTEMPTS
    headers = {'X-API-KEY': credentials['api_key']}
    while True:
        method = method.lower()
        if method == 'get':
            resp = get(url, headers=headers)
            
        elif method == 'post':
            if 'json' not in kwargs:
                raise JsonNeeded
            else:
                resp = post(url, json=kwargs['json'], headers=headers)

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