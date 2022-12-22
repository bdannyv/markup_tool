import json
import uuid

import aiohttp
from aiogram.dispatcher import FSMContext
from api.v1.buttons import greet_kb, inline_kb1
from bot_config import app_config
from core import bot


async def get_image_id(chat_id, state: FSMContext):
    """Get ID of unlabeled message"""
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f'http://{app_config.label_service.host}:{app_config.label_service.port}/markup/v1/unlabeled'
        ) as response:
            if response.status == 204:
                await bot.send_message(chat_id=chat_id, text="There is no images for labeling", reply_markup=greet_kb)
                return

            body = json.loads(await response.content.read())
            await state.update_data(image_id=body['id'])

            return body


async def send_image_(chat_id, id: uuid.UUID):
    """Get image by id and send it to bot"""
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f'http://{app_config.label_service.host}:{app_config.label_service.port}/markup/v1/image/{id}'
        ) as response:
            img = await response.read()

            await bot.send_photo(chat_id, img, reply_markup=inline_kb1)


async def render_image(chat_id, state: FSMContext):
    """Render image"""
    body = await get_image_id(chat_id=chat_id, state=state)
    await send_image_(chat_id=chat_id, id=body['id'])


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
                await render_image(state=state, chat_id=chat_id)
