from aiogram import types
from aiogram.dispatcher import FSMContext
from api.v1.buttons import greet_kb
from core import dp


@dp.message_handler(lambda c: c.text in ('Cancel', "Exit"), state='*')
async def cancel_button(message: types.Message, state: FSMContext):
    await state.reset_state()
    await message.answer(message.text, reply_markup=greet_kb)
