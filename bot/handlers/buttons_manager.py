from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_menu_buttons():
    today_btn = KeyboardButton(text="Сегодня")
    tomorrow_btn = KeyboardButton(text="Завтра")
    this_week_btn = KeyboardButton(text="Эта неделя")
    next_week_btn = KeyboardButton(text="Следующая неделя")
    buttons = [
        [today_btn, tomorrow_btn],
        #[this_week_btn, next_week_btn]
    ]

    keyboard = ReplyKeyboardMarkup(keyboard=buttons,
                                   resize_keyboard=True)
    return keyboard


def yes_or_no_buttons():
    yes_btn = KeyboardButton(text="Да")
    no_btn = KeyboardButton(text="Нет")
    buttons = [
        [yes_btn], [no_btn]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=buttons,
                                   resize_keyboard=True,
                                   one_time_keyboard=True)
    return keyboard


def approve_buttons():
    yes_btn = KeyboardButton(text="Все верно")
    cancel_btn = KeyboardButton(text="Отменить добавление")
    rework_btn = KeyboardButton(text="Настроить заново")
    buttons = [
        [yes_btn],
        [cancel_btn],
        [rework_btn],
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard