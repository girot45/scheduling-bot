from datetime import datetime

from aiogram import types, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot.States import UserData
from bot.database.db_manager import db_connect
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
    F.text.regexp("^([0-1]\d|2[0-3])(:[0-5]\d){1}$")
)
async def timestart(message: types.Message, state: FSMContext):
    await state.update_data(TimeStart=message.text)

    await message.answer("Введите время окончания (например, 15:00)")
    await state.set_state(UserData.TimeEnd)


@add_event_router.message(
    UserData.TimeEnd,
    F.text.regexp("^([0-1]\d|2[0-3])(:[0-5]\d){1}$")
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
    await message.reply("Вы ввели событие. Оно будет повторяться "
                        "каждую неделю?")
    await state.set_state(UserData.IsRepeat)


@add_event_router.message(
    UserData.IsRepeat,
    F.text
)
async def isrepeat(message: types.Message, state: FSMContext):
    await state.update_data(IsRepeat=message.text)
    user_data = await state.get_data()
    await message.answer("Проверьте введенные вами данные")
    await message.answer(
        f"{user_data['Date']}\n"
        f"{user_data['TimeStart']}\n"
        f"{user_data['TimeEnd']}\n\n"
        f"{user_data['Event']}\n\n"
        f"{user_data['IsRepeat']}\n"
    )
    # for case in user_data.items():
    #     await message.answer(f"{user_data[case]}")
    await state.set_state(UserData.Approve)


@add_event_router.message(
    UserData.Approve,
    F.text.lower().in_({"да", "нет"})
)
async def approve(
        message: types.Message,
        state: FSMContext
):
    await state.update_data(Approve=message.text)
    user_data = await state.get_data()
    if message.text.lower() == "да":
        isrepeat = 1
    else:
        isrepeat = 0

    data_to_db = {
        "tg_id": message.from_user.id,
        "Date": user_data['Date'],
        "TimeStart": user_data['TimeStart'],
        "TimeEnd": user_data['TimeEnd'],
        "Event": user_data['Event'],
        "IsRepeat": isrepeat,
    }
    session = await db_connect.get_session()
    res = await insert_event(data_to_db, session)
    await state.clear()