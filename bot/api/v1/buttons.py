import json

import aiohttp
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)
from bot_config import app_config

# Common buttons
inline_cancel = KeyboardButton('Cancel')
cancel = ReplyKeyboardMarkup().row(inline_cancel)


# Initial buttons
register_button = KeyboardButton('Sign In')
login_button = KeyboardButton('Sign Up')
label_button = KeyboardButton('Start labeling')

greet_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
greet_kb.add(register_button)
greet_kb.add(login_button)
greet_kb.add(label_button)
greet_kb.add(inline_cancel)

# authentication
inline_singin = KeyboardButton('Submit')
proceed = ReplyKeyboardMarkup().row(inline_singin).row(inline_cancel)

# markups

inline_kb1 = InlineKeyboardMarkup()


async def retrieve_classes(incognito):
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f"http://{app_config.label_service.host}:{app_config.label_service.port}/markup/v1/class/"
        ) as response:
            if response.status == 200:
                class_list = json.loads(await response.content.read())
                for cl in class_list:
                    inline_btn = InlineKeyboardButton(cl, callback_data=cl)
                    inline_kb1.add(inline_btn)
