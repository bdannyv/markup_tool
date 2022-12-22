from aiogram import types
from aiogram.dispatcher import FSMContext
from api.v1.handlers.utils.auth import (Action, authenticate,
                                        authentication_start,
                                        password_input_body,
                                        username_input_body)
from core import dp
from pydantic import EmailError, EmailStr
from states import authentication


@dp.message_handler(lambda c: c.text == 'Sign Up', state='*')
async def register_button(message: types.Message, state: FSMContext):
    """Handle Sing In input"""
    await authentication_start(
        message=message,
        state=state,
        status=authentication.SignupInputStates.username,
    )


@dp.message_handler(lambda c: c.text == 'Sign In', state='*')
async def signin_button(message: types.Message, state: FSMContext):
    """Handle Sing Up input"""
    await authentication_start(
        message=message,
        state=state,
        status=authentication.SignInInputStates.username
    )


@dp.message_handler(state=authentication.SignupInputStates.username)
async def username_input(message: types.Message, state: FSMContext):
    """Poll for username in sign in flow"""
    await username_input_body(
        message=message,
        state=state,
        status=authentication.SignupInputStates.email,
        input_type='email'
    )


@dp.message_handler(state=authentication.SignInInputStates.username)
async def username_input_signin(message: types.Message, state: FSMContext):
    """Poll for username in sign up flow"""
    await username_input_body(
        message=message,
        state=state,
        status=authentication.SignInInputStates.password,
        input_type='password'
    )


@dp.message_handler(state=authentication.SignupInputStates.email)
async def email_input(message: types.Message, state: FSMContext):
    """Poll for email in sign in flow with validation"""
    try:
        validated = EmailStr.validate(message.text)
    except EmailError:
        await message.reply("Wrong email format")
        return

    await state.update_data(email=validated)
    await state.set_state(authentication.SignupInputStates.password)
    await message.reply("Waiting for password")


@dp.message_handler(state=authentication.SignupInputStates.password)
async def password_input(message: types.Message, state: FSMContext):
    """Poll for password in sign in flow"""
    await password_input_body(
        message=message,
        state=state,
        status=authentication.SignupInputStates.action
    )


@dp.message_handler(state=authentication.SignInInputStates.password)
async def password_input_signin(message: types.Message, state: FSMContext):
    """Poll for password in sign up flow"""
    await password_input_body(
        message=message,
        state=state,
        status=authentication.SignInInputStates.action
    )


@dp.message_handler(
    lambda x: x.text == "Submit",
    state=[authentication.SignupInputStates.action, authentication.SignInInputStates.action]
)
async def signup(message: types.Message, state: FSMContext):
    """Finish of authentication"""
    st = await state.get_state()
    await authenticate(
        state=state,
        message=message,
        action=Action.signup if st == 'SignupInputStates:action' else Action.signin
    )
