import enum
import json

import aiohttp
from aiogram import types
from aiogram.dispatcher import FSMContext
from api.v1.buttons import cancel, greet_kb, proceed
from bot_config import app_config
from states import user


class Action(enum.Enum):
    signin = 0
    signup = 1


async def authentication_start(
        message: types.Message,
        state: FSMContext,
        status
):
    """Start of sign"""
    await message.reply('Waiting for username', reply_markup=cancel)
    await state.set_state(status)


async def username_input_body(
        message: types.Message,
        state: FSMContext,
        input_type: str,
        status
):
    """Save username to state and start polling for email"""
    await state.update_data(username=message.text)
    await message.reply(f'Waiting for {input_type}')
    await state.set_state(status)


async def password_input_body(
        state: FSMContext,
        message: types.Message,
        status
):
    await state.update_data(password=message.text)
    await state.set_state(status)
    data = await state.get_data()
    await message.reply(
        ', '.join([f'{row}: {data[row]}' for row in data]),  # unpacking dict to str
        reply_markup=proceed
    )


async def authenticate(state: FSMContext, message: types.Message, action: Action):
    async with aiohttp.ClientSession() as session:
        data = await state.get_data()
        async with session.post(
                f"http://{app_config.label_service.host}:{app_config.label_service.port}/auth/v1/{action.name}",
                data=json.dumps({key: data[key] for key in data}),
        ) as response:
            if response.status == 200:
                await state.set_state(user.UserStates.authenticated)
                msg = "Success"
            else:
                await state.reset_state()
                msg = "Failed"

            await message.reply(msg, reply_markup=greet_kb)
