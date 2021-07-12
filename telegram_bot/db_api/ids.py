import enum

class Events(enum.IntEnum):
    lock_state_change = enum.auto()
    user_login = enum.auto()
    entry = enum.auto()
    user_change = enum.auto()

class Settings(enum.IntEnum):
    lock = enum.auto()
    ltime_report = enum.auto()
    ontime_report = enum.auto()