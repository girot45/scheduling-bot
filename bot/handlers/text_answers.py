import datetime

from aiogram import types, F, Router

from bot.database.db_manager import db_connect
from bot.queries.one_day_select import query_events_by_tg_id

router_text = Router()

@router_text.message(F.text.lower().in_({"сегодня", "завтра"}))
async def answer_message_today(message: types.Message):
    session = await db_connect.get_session()
    date_ = datetime.date.today()
    if message.text.lower() == "завтра":
        date_ += datetime.timedelta(days=1)
    res = await query_events_by_tg_id(
        session,
        message.from_user.id,
        date_
    )

    await message.answer(res)


waiting_for_input = {}

@router_text.message(F.text.in_({"Выбрать дату"}))
async def answer_message_today(message: types.Message):
    if message.from_user.id not in waiting_for_input:
        waiting_for_input[message.from_user.id] = True
        await message.answer("Привет! Введите какие-либо данные:")
    else:
        await message.answer("Вы уже вводите данные.")



@router_text.message(
    lambda message: waiting_for_input.get(message.from_user.id),
    F.text.regexp(
        "[0-9]{4}-(0[1-9]|1[012])-(0[1-9]|1[0-9]|2[0-9]|3[01])"))
async def input_received(message: types.Message):
    user_input = message.text
    # Обрабатывайте введенные данные и выполняйте необходимую логику
    await message.answer(f"Вы ввели: {user_input}")
    # Сбросьте флаг ожидания
    waiting_for_input[message.from_user.id] = False

    session = await db_connect.get_session()
    date_ = datetime.datetime.strptime(user_input, "%Y-%m-%d")
    res = await query_events_by_tg_id(
        session,
        message.from_user.id,
        date_
    )

    await message.answer(res)