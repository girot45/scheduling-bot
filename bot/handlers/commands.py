from datetime import datetime

from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from bot.States import UserData


router_commands = Router()

@router_commands.message(Command("start"))
async def start(message: types.Message):
    print(message.chat.id)
    print(datetime.weekday(datetime.now()))
    await message.answer("Привет. Нажми на /menu.")

