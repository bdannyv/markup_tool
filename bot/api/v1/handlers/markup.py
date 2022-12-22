from aiogram import types
from aiogram.dispatcher import FSMContext
from api.v1.buttons import greet_kb, image_classes
from api.v1.commands import retrieve_classes
from api.v1.handlers.utils.mark import post_label, render_image
from core import bot, dp


@dp.message_handler(lambda x: x.text == 'Start labeling', state='*')
async def labeling(message: types.Message, state: FSMContext):
    await retrieve_classes()

    state_check = await state.get_state()

    if state_check != 'UserStates:authenticated':
        await message.reply(
            "You are not authenticated. Push Sign In/Up",
            reply_markup=greet_kb
        )
        return

    await render_image(state=state, chat_id=message.from_user.id)


@dp.callback_query_handler(lambda c: c.data in image_classes, state="*")
async def process_callback_button1(callback_query: types.CallbackQuery, state: FSMContext):
    await retrieve_classes()

    state_check = await state.get_state()

    if state_check != 'UserStates:authenticated':
        await bot.send_message(
            callback_query.from_user.id,
            'You are not authenticated. Push Sign In/Up',
            reply_markup=greet_kb
        )
        return

    await state.update_data(type=callback_query.data)
    await post_label(state=state, chat_id=callback_query.from_user.id)
