import time
from datetime import datetime, date

from aiogram import types, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot.States import UserData
from bot.database.db_manager import db_connect
from bot.handlers.buttons_manager import (
    yes_or_no_buttons,
    approve_buttons,
    main_menu_buttons,
    dont_need_button
)
from bot.messages.messages_texts import *
from bot.queries.insert_event import insert_event


add_event_router = Router()


@add_event_router.message(Command("add_event"))
async def add_event(message: types.Message, state: FSMContext):
    await message.answer(f"{ADD_NEW_EVENT} {WRITE_DATE_MES}")
    await state.set_state(UserData.Date)


@add_event_router.message(
    UserData.Date,
    F.text.regexp(
        "[0-9]{4}-(0[1-9]|1[012])-(0[1-9]|1[0-9]|2[0-9]|3[01])")
)
async def add_date(message: types.Message, state: FSMContext):
    try:
        if date.fromisoformat(message.text.lower()):
            pass
        await state.update_data(Date=message.text.lower())

        await message.answer(WRITE_TIMESTART_MES)
        await state.set_state(UserData.TimeStart)
    except ValueError:
        await message.answer("Такой даты несуществует. Введите дату корректно")
        return


@add_event_router.message(UserData.Date)
async def date_incorrectly(message: types.Message):
    await message.answer(ADD_DATE_ERROR_FORMAT_MES)


@add_event_router.message(
    UserData.TimeStart,
    F.text.regexp("^([01]?[0-9]|2[0-3]):[0-5][0-9]$")
)
async def timestart(message: types.Message, state: FSMContext):
    await state.update_data(TimeStart=message.text)

    await message.answer(WRITE_TIMEEND_MES,
                         reply_markup=dont_need_button())
    await state.set_state(UserData.TimeEnd)


@add_event_router.message(
    UserData.TimeEnd,
    F.text.regexp("^([01]?[0-9]|2[0-3]):[0-5][0-9]$")
)
async def timeend(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    if datetime.strptime(message.text, "%H:%M") <= \
            datetime.strptime(user_data["TimeStart"], "%H:%M"):
        await message.answer(ADD_TIME_VALUE_ERROR)
        return
    await state.update_data(TimeEnd=message.text)

    await message.reply(WRITE_EVENT_MES)
    await state.set_state(UserData.Event)


@add_event_router.message(
    UserData.TimeEnd,
    F.text.in_({"Не нужно"})
)
async def timeend_dont_need(
        message: types.Message, state: FSMContext
):
    await state.update_data(TimeEnd=None)

    await message.reply(WRITE_EVENT_MES)
    await state.set_state(UserData.Event)


@add_event_router.message(UserData.TimeStart or UserData.TimeEnd)
async def time_incorrect(message: types.Message):
    await message.answer(ADD_TIME_FORMAT_ERROR_MES)


@add_event_router.message(UserData.Event, F.text)
async def event(message: types.Message, state: FSMContext):
    await state.update_data(Event=message.text)
    await message.reply(
        WRITE_ISREPEAT_MES,
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
    if not user_data['TimeEnd']:
        timeend_ = "Не нужно"
    else:
        timeend_ = user_data['TimeEnd']
    await message.answer(EVENTED_CREATED_MES)
    await message.answer(
        "Проверьте введенные вами данные\n\n"
        f"Дата: {user_data['Date']}\n"
        f"Время начала: {user_data['TimeStart']}\n"
        f"Время окончания: {timeend_}\n\n"
        f"Описание события:\n{user_data['Event']}\n\n"
        f"Повторятся: {message.text.lower()}\n",
        reply_markup=approve_buttons()
    )
    await state.set_state(UserData.Approve)


@add_event_router.message(UserData.IsRepeat)
async def isrepeat(message: types.Message):
    await message.answer(
        ADD_ISREPEAT_ERROR_MES,
        reply_markup=yes_or_no_buttons(),
    )


@add_event_router.message(
    UserData.Approve,
    F.text.in_(
        {"Все верно", "Отменить добавление", "Настроить заново"})
)
async def approve(
        message: types.Message,
        state: FSMContext
):
    await state.update_data(Approve=message.text)
    user_data = await state.get_data()
    await state.clear()

    if message.text == "Отменить добавление":
        await message.answer(CANCEL_CREATION_OF_EVENT)
        time.sleep(0.5)
        await message.answer("Меню", reply_markup=main_menu_buttons())
    elif message.text == "Настроить заново":
        await message.answer(
            F"{ADD_EVENT_AGAIN_MES} {WRITE_DATE_MES}")
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
        await message.answer(WRITE_EVENT_TO_DB_MES)
        session = await db_connect.get_session()
        res = await insert_event(data_to_db, session)
        if res:
            answer_str = WRITE_EVENT_TO_DB_SUCCESS_MES
        else:
            answer_str = WRITE_EVENT_TO_DB_ERROR_MES
        await message.answer(answer_str)
        await message.answer("Меню", reply_markup=main_menu_buttons())


@add_event_router.message(UserData.Approve)
async def approve_incorrect(message: types.Message):
    await message.answer(
        APPROVE_EVENT_FORMAT_ERROR,
        reply_markup=approve_buttons()
    )
