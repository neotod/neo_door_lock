import enum

class Events(enum.IntEnum):
    lock_state_change = enum.auto()
    user_login = enum.auto()
    entry = enum.auto()
    user_change = enum.auto()