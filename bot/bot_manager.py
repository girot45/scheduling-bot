import os

from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage


TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

storage = MemoryStorage()
bot = Bot(token=TELEGRAM_TOKEN, parse_mode='HTML')
dp = Dispatcher(storage=storage)