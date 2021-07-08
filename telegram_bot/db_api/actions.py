import jdatetime

from . import ids
from .utils import *

def init(config):
    update_credentials(config['username'], config['password'])

def read(json):
    url = URLs['read']
    res = send_request(url, json)
    return res['result']

def insert(json):
    url = URLs['insert']
    res = send_request(url, json)
    return res['result']

def update(json):
    url = URLs['update']
    res = send_request(url, json)
    return res['result']

def delete(json):
    url = URLs['delete']
    res = send_request(url, json)
    return res['result']

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