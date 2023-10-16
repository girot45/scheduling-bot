
from aiogram import types, Router
from aiogram.filters import Command
from bot.handlers.buttons_manager import main_menu_buttons


router_commands = Router()


@router_commands.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "Меню",
        reply_markup=main_menu_buttons()
    )
