from .ids import Buttons, Pages

class Button:
    def __init__(self, id_: Buttons, text: str, next_page_id: int, row_index: int=0):
        self.id_ = id_
        self.text = text
        self.next_page_id = next_page_id
        self.row_index = row_index

class Page:
    def __init__(self, id_: Pages, buttons: dict, description: str):
        self.id_ = id_
        self.buttons = buttons
        self.description = description

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