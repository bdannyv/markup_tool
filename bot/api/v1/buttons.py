from aiogram.types import (InlineKeyboardMarkup, KeyboardButton,
                           ReplyKeyboardMarkup)

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
image_classes = []
