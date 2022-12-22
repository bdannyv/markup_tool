import json

import aiohttp
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton
from api.v1 import buttons as kb
from api.v1.buttons import image_classes, inline_kb1  # noqa
from bot_config import app_config
from core import dp


# OMG
async def retrieve_classes():
    global image_classes
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f"http://{app_config.label_service.host}:{app_config.label_service.port}/markup/v1/class/"
        ) as response:
            if response.status == 200:
                cls = json.loads(await response.content.read())
                for cl in cls:
                    if cl not in image_classes:
                        image_classes.add(cl)
                        inline_btn = InlineKeyboardButton(cl, callback_data=cl)
                        inline_kb1.add(inline_btn)


@dp.message_handler(commands=['start'], state='*')
async def process_start_command(message: types.Message, state: FSMContext):
    await state.reset_state()
    await message.reply(
        f"Hi, {message.from_user.first_name} {message.from_user.last_name}!", reply_markup=kb.greet_kb
    )


@dp.message_handler(commands=['stop'], state='*')
async def process_stop_command(message: types.Message, state: FSMContext):
    await state.reset_state()
    await message.reply(
        f"Good Bye, {message.from_user.first_name} {message.from_user.last_name}!", reply_markup=kb.greet_kb
    )


@dp.message_handler(commands=['help'], state='*')
async def process_help_command(message: types.Message):
    await message.reply(
        "Main purpose of this bot is image labeling\nAvailable command /start, /stop, /help.\n"
        "This section will be complemented",
        reply_markup=kb.greet_kb
    )


@dp.message_handler(commands=['reset_state'], state='*')
async def reset_state(message: types.Message, state: FSMContext):
    await state.reset_state()


@dp.message_handler(commands=['state'], state='*')
async def get_state(message: types.Message, state: FSMContext):
    await message.reply(await state.get_state() or "No state")
