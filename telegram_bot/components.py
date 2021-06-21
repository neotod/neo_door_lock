import enum


class Events(enum.Enum):
    lock_state_change = enum.auto()
    user_login = enum.auto()
    user_change = enum.auto()
    entry = enum.auto()

class Smart_Lock:
    def __init__(self, state: bool=True, ontime_report_on: bool=False, longtime_report_on: bool=False, phone_number: int=0):
        self.on = state # true => lock is working, false => lock is not working
        self.oreport_on = ontime_report_on
        self.lreport_on = longtime_report_on
        self.phone_number = phone_number

class User:
    def __init__(self, telegram_obj, name: str, lastname: str, username:str, phone_number :int=0):
        self.telegram_obj = telegram_obj
        self.name = name
        self.lastname = lastname
        self.username = username
        self.phone_number = phone_number

class Event:
    def __init__(self, id_: Events, name: str):
        self.id_ = id_
        self.name = name