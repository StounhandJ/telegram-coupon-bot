from aiogram.dispatcher.filters.state import StatesGroup, State


class UserMes(StatesGroup):
    message = State()
    documentCheck = State()
    document = State()
    email = State()
    wait = State()