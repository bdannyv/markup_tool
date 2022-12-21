import json

import aiohttp
from aiogram import types
from aiogram.dispatcher import FSMContext
from api.v1.buttons import greet_kb, image_classes, inline_kb1
from api.v1.commands import retrieve_classes
from bot_config import app_config
from core import bot, dp


async def send_image(chat_id, state: FSMContext):
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f'http://{app_config.label_service.host}:{app_config.label_service.port}/markup/v1/unlabeled'
        ) as response:

            if response.status == 204:
                await bot.send_message(chat_id=chat_id, text="There is no images for labeling", reply_markup=greet_kb)
                return

            body = json.loads(await response.content.read())
            await state.update_data(image_id=body['id'])

        async with session.get(
                f'http://{app_config.label_service.host}:{app_config.label_service.port}/markup/v1/image/{body["id"]}'
        ) as response:
            img = await response.read()

            await bot.send_photo(chat_id, img, reply_markup=inline_kb1)


async def post_label(state: FSMContext, chat_id):
    async with aiohttp.ClientSession() as session:
        data = await state.get_data()
        async with session.post(
            f'http://{app_config.label_service.host}:{app_config.label_service.port}/markup/v1/labeled/',
            data=json.dumps({
                "user_name": data['username'],
                "image_id": data['image_id'],
                "type": data['type'],
            })
        ) as response:
            if response.status == 200:
                await send_image(state=state, chat_id=chat_id)


@dp.message_handler(lambda x: x.text == 'Start labeling', state='*')
async def labeling(message: types.Message, state: FSMContext):
    state_check = await state.get_state()

    if state_check != 'UserStates:authenticated':
        await message.reply("You are not authenticated", reply_markup=greet_kb)
        return

    await send_image(state=state, chat_id=message.from_user.id)


@dp.callback_query_handler(lambda c: c.data in image_classes, state="*")
async def process_callback_button1(callback_query: types.CallbackQuery, state: FSMContext):
    await retrieve_classes()

    state_check = await state.get_state()

    if state_check != 'UserStates:authenticated':
        await bot.send_message(callback_query.from_user.id, 'Unauthorized', reply_markup=greet_kb)
        return
    await state.update_data(type=callback_query.data)
    await post_label(state=state, chat_id=callback_query.from_user.id)
