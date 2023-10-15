from datetime import datetime

from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from bot.States import UserData
from bot.handlers.buttons_manager import main_menu_buttons

router_commands = Router()

@router_commands.message(Command("start"))
async def start(message: types.Message):

    await message.answer(
        "Главное меню",
        reply_markup=main_menu_buttons()
    )

