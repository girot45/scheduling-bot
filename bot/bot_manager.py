from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage

from bot.config import TELEGRAM_TOKEN


storage = MemoryStorage()
bot = Bot(token=TELEGRAM_TOKEN, parse_mode='HTML')
dp = Dispatcher(storage=storage)