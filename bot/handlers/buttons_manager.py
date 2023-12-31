from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    WebAppInfo


def main_menu_buttons() -> ReplyKeyboardMarkup:
    today_btn = KeyboardButton(text="Сегодня")
    tomorrow_btn = KeyboardButton(text="Завтра")
    kb = KeyboardButton(text="Перейти",
                        web_app=WebAppInfo(url="https://calendar.yandex.ru/event?moreParams=1"))
    # this_week_btn = KeyboardButton(text="Эта неделя")
    # next_week_btn = KeyboardButton(text="Следующая неделя")
    choose_date_btn = KeyboardButton(text="Выбрать дату")
    buttons = [
        [today_btn, tomorrow_btn],
        # [this_week_btn, next_week_btn]
        [choose_date_btn],
        [kb]
    ]

    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )
    return keyboard


def yes_or_no_buttons() -> ReplyKeyboardMarkup:
    yes_btn = KeyboardButton(text="Да")
    no_btn = KeyboardButton(text="Нет")
    buttons = [
        [yes_btn], [no_btn]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard


def approve_buttons() -> ReplyKeyboardMarkup:
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


def dont_need_button() -> ReplyKeyboardMarkup:
    dont_need_btn = KeyboardButton(text="Не нужно")
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[dont_need_btn]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard
