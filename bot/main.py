import logging

from aiogram import executor
from api.v1 import commands, handlers  # noqa
from core import dp

logging.basicConfig(level=logging.INFO)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
