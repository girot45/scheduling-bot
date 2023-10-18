from aiogram.filters.state import StatesGroup, State


class UserData(StatesGroup):
    Date = State()
    TimeStart = State()
    TimeEnd = State()
    Event = State()
    IsRepeat = State()
    Approve = State()
