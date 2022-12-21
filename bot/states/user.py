from aiogram.dispatcher.filters.state import State, StatesGroup


class UserStates(StatesGroup):

    AUTHENTICATED = State()
    NOT_AUTHENTICATED = State()
