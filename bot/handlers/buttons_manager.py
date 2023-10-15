from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_menu_buttons():

    today_btn = KeyboardButton(text="Сегодня")
    tomorrow_btn = KeyboardButton(text="Завтра")
    this_week_btn = KeyboardButton(text="Эта неделя")
    next_week_btn = KeyboardButton(text="Следующая неделя")
    buttons = [
        [today_btn, tomorrow_btn],
        [this_week_btn, next_week_btn]
    ]

    keyboard = ReplyKeyboardMarkup(keyboard=buttons,
                                   resize_keyboard=True)
    return keyboard