import time
from datetime import datetime

from aiogram import types, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot.States import UserData
from bot.database.db_manager import db_connect
from bot.handlers.buttons_manager import yes_or_no_buttons, \
    approve_buttons, main_menu_buttons
from bot.queries.insert_event import insert_event

add_event_router = Router()


@add_event_router.message(Command("add_event"))
async def add_event(message: types.Message, state: FSMContext):
    # Set the state to Date
    await message.answer(
        "Давайте добавим новое событие. Введите дату в формате "
        "ГГГГ-ММ-ДД")
    await state.set_state(UserData.Date)


@add_event_router.message(
    UserData.Date,
    F.text.regexp(
        "[0-9]{4}-(0[1-9]|1[012])-(0[1-9]|1[0-9]|2[0-9]|3[01])")
)
async def date(message: types.Message, state: FSMContext):
    await state.update_data(Date=message.text.lower())

    await message.reply(f"Вы ввели дату: {message.text}\n"
                        f"Теперь введите время начала (например, 12:00)")
    await state.set_state(UserData.TimeStart)


@add_event_router.message(UserData.Date)
async def date_incorrectly(message: types.Message):
    await message.answer("Дата введена некорректно")


@add_event_router.message(
    UserData.TimeStart,
    F.text.regexp("^([01]?[0-9]|2[0-3]):[0-5][0-9]$")
)
async def timestart(message: types.Message, state: FSMContext):
    await state.update_data(TimeStart=message.text)

    await message.answer("Введите время окончания (например, 15:00)")
    await state.set_state(UserData.TimeEnd)


@add_event_router.message(
    UserData.TimeEnd,
    F.text.regexp("^([01]?[0-9]|2[0-3]):[0-5][0-9]$")
)
async def timeend(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    if datetime.strptime(message.text, "%H:%M") <= \
            datetime.strptime(user_data["TimeStart"], "%H:%M"):
        await message.answer("Время окончания не может быть меньше "
                             "времени начала")
        return
    await state.update_data(TimeEnd=message.text)

    await message.reply(f"Вы ввели время окончания:"
                        f" {message.text}\nТеперь введите событие")
    await state.set_state(UserData.Event)


@add_event_router.message(
    UserData.TimeStart or UserData.TimeEnd
)
async def time_incorrect(message: types.Message):
    await message.answer("Время введено некорректно")


@add_event_router.message(
    UserData.Event,
    F.text
)
async def event(message: types.Message, state: FSMContext):
    await state.update_data(Event=message.text)
    await message.reply(
        "Вы ввели событие. Оно будет повторяться каждую неделю?",
        reply_markup=yes_or_no_buttons()
    )
    await state.set_state(UserData.IsRepeat)


@add_event_router.message(
    UserData.IsRepeat,
    F.text.lower().in_({"да", "нет"})
)
async def isrepeat(message: types.Message, state: FSMContext):
    if message.text.lower() == "да":
        isRepeat = 1
    else:
        isRepeat = 0
    await state.update_data(IsRepeat=isRepeat)
    user_data = await state.get_data()
    await message.answer(
        "Проверьте введенные вами данные\n\n"
        f"Дата: {user_data['Date']}\n"
        f"Время начала: {user_data['TimeStart']}\n"
        f"Время окончания: {user_data['TimeEnd']}\n\n"
        f"Описание события:\n{user_data['Event']}\n\n"
        f"Повторятся: {message.text.lower()}\n",
        reply_markup=approve_buttons()
    )
    # for case in user_data.items():
    #     await message.answer(f"{user_data[case]}")
    await state.set_state(UserData.Approve)


@add_event_router.message(
    UserData.IsRepeat)
async def isrepeat(message: types.Message):
    await message.answer(
        'Введите <b>Да</b> или <b>Нет</b>, или воспользуйтесь клавиатурой',
        reply_markup=yes_or_no_buttons(),
    )



@add_event_router.message(
    UserData.Approve,
    F.text.in_({"Все верно", "Отменить добавление", "Настроить заново"})
)
async def approve(
        message: types.Message,
        state: FSMContext
):
    await state.update_data(Approve=message.text)
    user_data = await state.get_data()
    await state.clear()

    if message.text == "Отменить добавление":
        await message.answer("Добавление события отменено")
        time.sleep(0.5)
        await message.answer("Меню", reply_markup=main_menu_buttons())
    elif message.text == "Настроить заново":
        await message.answer(
            "Давайте попробуем еще раз. Введите дату в формате "
            "ГГГГ-ММ-ДД")
        await state.set_state(UserData.Date)
    else:
        data_to_db = {
            "tg_id": message.from_user.id,
            "Date": user_data['Date'],
            "TimeStart": user_data['TimeStart'],
            "TimeEnd": user_data['TimeEnd'],
            "Event": user_data['Event'],
            "IsRepeat": user_data['IsRepeat'],
        }
        session = await db_connect.get_session()
        res = await insert_event(data_to_db, session)
        await message.answer("Вы успешно добавили событие")
        await message.answer("Меню", reply_markup=main_menu_buttons())


@add_event_router.message(UserData.Approve)
async def approve_incorrect(message: types.Message):
    await message.answer("Для подтверждения воспользуйтесь "
                         "клавиатурой")