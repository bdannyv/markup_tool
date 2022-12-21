import json

import aiohttp
from aiogram import types
from aiogram.dispatcher import FSMContext
from api.v1.buttons import cancel, greet_kb, proceed
from bot_config import app_config
from core import dp
from pydantic import EmailError, EmailStr
from states import authentication, user


@dp.message_handler(lambda c: c.text == 'Cancel', state='*')
async def cancel_button(message: types.Message, state: FSMContext):
    await state.reset_state()
    await message.reply('Canceled', reply_markup=greet_kb)


@dp.message_handler(lambda c: c.text == 'Sign Up', state='*')
async def register_button(message: types.Message, state: FSMContext):
    await message.reply('Waiting for username', reply_markup=cancel)
    await state.set_state(authentication.SignupInputStates.username)


@dp.message_handler(state=authentication.SignupInputStates.username)
async def username_input(message: types.Message, state: FSMContext):
    await state.update_data(username=message.text)
    await message.reply('Waiting for email')
    await state.set_state(authentication.SignupInputStates.email)


@dp.message_handler(state=authentication.SignupInputStates.email)
async def email_input(message: types.Message, state: FSMContext):
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
    await state.update_data(password=message.text)
    await state.set_state(authentication.SignupInputStates.action)
    data = await state.get_data()
    await message.reply(
        f"username: {data.get('username')}, "
        f"password: {data.get('password')}, "
        f"email: {data.get('email')}",
        reply_markup=proceed
    )


@dp.message_handler(lambda x: x.text == "Submit", state=authentication.SignupInputStates.action)
async def signup(message: types.Message, state: FSMContext):
    async with aiohttp.ClientSession() as session:
        data = await state.get_data()
        async with session.post(
            f"http://{app_config.label_service.host}:{app_config.label_service.port}/auth/v1/signup",
            data=json.dumps({
                'username': data.get('username'),
                'password': data.get('password'),
                'email': data.get('email'),
            }),
        ) as response:
            if response.status == 200:
                await state.reset_data()
                await state.set_state(user.UserStates.AUTHENTICATED)
                msg = "Success"
            else:
                await state.reset_state()
                msg = "Failed"

            await message.reply(msg, reply_markup=greet_kb)


# TODO: Smells bad
@dp.message_handler(lambda c: c.text == 'Sign In', state='*')
async def signin_button(message: types.Message, state: FSMContext):
    await message.reply('Waiting for username', reply_markup=cancel)
    await state.set_state(authentication.SignInInputStates.username)


@dp.message_handler(state=authentication.SignInInputStates.username)
async def username_input_signin(message: types.Message, state: FSMContext):
    await state.update_data(username=message.text)
    await message.reply("Waiting for password")
    await state.set_state(authentication.SignInInputStates.password)


@dp.message_handler(state=authentication.SignInInputStates.password)
async def password_input_signin(message: types.Message, state: FSMContext):
    await state.update_data(password=message.text)
    data = await state.get_data()
    await message.reply(
        f"username: {data.get('username')}, "
        f"password: {data.get('password')}",
        reply_markup=proceed
    )
    await state.set_state(authentication.SignInInputStates.action)


@dp.message_handler(lambda x: x.text == "Submit", state=authentication.SignInInputStates.action)
async def signin(message: types.Message, state: FSMContext):
    async with aiohttp.ClientSession() as session:
        data = await state.get_data()
        async with session.post(
                f"http://{app_config.label_service.host}:{app_config.label_service.port}/auth/v1/signin",
                data=json.dumps({
                    'username': data.get('username'),
                    'password': data.get('password'),
                })
        ) as response:
            if response.status == 200:
                await state.reset_data()
                await state.set_state(user.UserStates.AUTHENTICATED)
                msg = 'Success'
            else:
                await state.reset_state()
                msg = 'Failed'

            await message.reply(msg, reply_markup=greet_kb)
