from aiogram.filters.state import StatesGroup, State


class AddEventStates(StatesGroup):
    date = State()
    time_start = State()
    time_end = State()
    event = State()
    is_repeat = State()
    approve = State()


class DeleteEventStates(StatesGroup):
    date_or_weekday = State()
    date = State()
    weekday = State()
