from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)

# Initial buttons
register_button = KeyboardButton('Sign In')
login_button = KeyboardButton('Sign Up')
label_button = KeyboardButton('Start labeling')

greet_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
greet_kb.add(register_button)
greet_kb.add(login_button)
greet_kb.add(label_button)

# authentication
inline_cancel = KeyboardButton('Cancel')
cancel = ReplyKeyboardMarkup().row(inline_cancel)

inline_singin = KeyboardButton('Submit')
proceed = ReplyKeyboardMarkup().row(inline_singin).row(inline_cancel)


# markups
inline_btn_1 = InlineKeyboardButton('Cat', callback_data='button1')
inline_btn_2 = InlineKeyboardButton('Dog', callback_data='button2')
inline_btn_3 = InlineKeyboardButton('CatDog', callback_data='button3')
inline_kb1 = InlineKeyboardMarkup().row(inline_btn_1).row(inline_btn_2).add(inline_btn_3)
