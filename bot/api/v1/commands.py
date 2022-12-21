from aiogram import types
from aiogram.dispatcher import FSMContext
from api.v1 import buttons as kb
from core import dp


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message, state: FSMContext):
    await state.reset_state()
    await message.reply(
        f"Hi, {message.from_user.first_name} {message.from_user.last_name}!", reply_markup=kb.greet_kb
    )


@dp.message_handler(commands=['stop'])
async def process_stop_command(message: types.Message, state: FSMContext):
    await state.reset_state()
    await message.reply(
        f"Good Bye, {message.from_user.first_name} {message.from_user.last_name}!", reply_markup=kb.greet_kb
    )


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply(
        "Main purpose of this bot is image labeling\nAvailable command /start, /stop, /help.\n"
        "This section will be complemented",
        reply_markup=kb.greet_kb
    )


@dp.message_handler(commands=['reset_state'])
async def reset_state(message: types.Message, state: FSMContext):
    await state.reset_state()
