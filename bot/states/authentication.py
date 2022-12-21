from aiogram.dispatcher.filters.state import State, StatesGroup


class AuthenticationStates(StatesGroup):
    signup = State()
    signin = State()


class SignInInputStates(StatesGroup):
    password = State()
    action = State()
    username = State()


class SignupInputStates(StatesGroup):
    password = State()
    action = State()
    username = State()
    email = State()
