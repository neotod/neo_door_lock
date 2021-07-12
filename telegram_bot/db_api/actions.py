import shutil
import jdatetime

from . import ids
from .utils import *

def init(config):
    update_credentials(config['username'], config['password'])

def read(json):
    url = URLs['db']['read']
    res = send_req(url, 'POST', json=json)
    return res['result']

def insert(json):
    url = URLs['db']['insert']
    res = send_req(url, 'POST', json=json)
    return res['result']

def update(json):
    url = URLs['db']['update']
    res = send_req(url, 'POST', json=json)
    return res['result']

def delete(json):
    url = URLs['db']['delete']
    res = send_req(url, 'POST', json=json)
    return res['result']

def backup():
    url = URLs['db']['backup']
    headers = {'X-API-KEY': credentials['api_key']}
    try:
        with get(url, headers=headers, stream=True) as r:
            with open('datas/backup.db', 'wb') as f:
                shutil.copyfileobj(r.raw, f)
    except:
        logger.exception("Can't get the backup file.")
        return False

    return True

def report(event_id: ids.Events, more_info: str):
    now_date = str(jdatetime.datetime.now().date())
    now_time = str(jdatetime.datetime.now().time())[:-7]

    data = {
        'reports': {
            'cols': ['event_id', 'date', 'time', 'more_info'], 
            'vals': [int(event_id), now_date, now_time, more_info]
        }
    }
    res = insert(data)
    return res

def sync(data=None):
    '''
    if data == None then it will get sync info from the db_server
    data = {'id': <setting_id>, 'is_on': <setting_state>}
    '''

    if data:
        res = send_req(URLs['sync'], 'POST', json=data)
    else:
        res = send_req(URLs['sync'], 'GET')

    return res['result']