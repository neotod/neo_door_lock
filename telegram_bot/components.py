class Smart_Lock:
    def __init__(self, state: bool=True, ontime_report_on: bool=False, longtime_report_on: bool=False, phone_number: int=0):
        self.on = state # true => lock is working, false => lock is not working
        self.oreport_on = ontime_report_on
        self.lreport_on = longtime_report_on
        self.phone_number = phone_number

class User:
    def __init__(self, name, lastname, username, phone_number=0):
        self.name = name
        self.lastname = lastname
        self.username = username
        self.phone_number = phone_number