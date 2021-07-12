import enum

class Pages(enum.Enum):
    welcome = enum.auto()

    login_username = enum.auto()
    login_password = enum.auto()

    main = enum.auto()
    settings = enum.auto()
    report = enum.auto()
    db = enum.auto()

    settings_report = enum.auto()
    settings_lock = enum.auto()

class Buttons(enum.IntEnum): # every button except back button in the bot, has a unique id
    back = enum.auto()
    login = enum.auto()
    logout = enum.auto()
    
    report = enum.auto()
    db = enum.auto()
    settings = enum.auto()

    settings_report = enum.auto()
    settings_lock = enum.auto()

    db_backup = enum.auto()

    day_report = enum.auto()
    month_report = enum.auto()
    year_report = enum.auto()
    
    settings_lreport_switch = enum.auto()
    settings_lreport_off = enum.auto()
    settings_lreport_on = enum.auto()

    settings_oreport_switch = enum.auto()
    settings_oreport_off = enum.auto()
    settings_oreport_on = enum.auto()

    settings_lock_switch = enum.auto()
    settings_lock_off = enum.auto()
    settings_lock_on = enum.auto()