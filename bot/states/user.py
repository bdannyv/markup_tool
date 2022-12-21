from aiogram.dispatcher.filters.state import State, StatesGroup


class UserStates(StatesGroup):
    authenticated = State()
    not_authenticated = State()
