import datetime
from typing import Optional

from aiogram import types, F, Router, Bot

from bot.database.db_manager import db_connect
from bot.messages.formating_messages import \
    formatting_a_day_schedule_for_sending_a_message
from bot.messages.messages_texts import WRITE_DATE_MES
from bot.queries.one_day_select import query_events_by_tg_id

router_text = Router()


@router_text.message(F.text.lower().in_({"сегодня", "завтра"}))
async def send_table_today_or_tomorrow(
        message: Optional[Bot | types.Message],
        chat_id: Optional[int] = None,
        istomorrow: Optional[bool] = None,
):
    session = await db_connect.get_session()
    date_ = datetime.date.today()
    message_type = type(message)
    if message_type == types.Message:
        send_id = message.from_user.id
    else:
        send_id = chat_id
    if (message_type == types.Message
         and message.text.lower() == "завтра") or istomorrow:
        date_ += datetime.timedelta(days=1)

    res = await query_events_by_tg_id(
        session,
        send_id,
        date_
    )
    message_to_user = formatting_a_day_schedule_for_sending_a_message(
        res,
        date_
    )
    if message_type == Bot:
        await message.send_message(
            chat_id=send_id,
            text=message_to_user
        )
    elif message_type == types.Message:
        await message.answer(message_to_user)


waiting_for_input = {}


@router_text.message(F.text.in_({"Выбрать дату"}))
async def send_message_on_date(message: types.Message):
    waiting_for_input[message.from_user.id] = True
    await message.answer(WRITE_DATE_MES)


@router_text.message(
    lambda message: waiting_for_input.get(message.from_user.id),
    F.text.regexp(
        "[0-9]{4}-(0[1-9]|1[012])-(0[1-9]|1[0-9]|2[0-9]|3[01])"))
async def input_received(message: types.Message):
    user_input = message.text
    try:
        if datetime.date.fromisoformat(user_input):
            pass
        await message.answer(f"Вы ввели: {user_input}")
        waiting_for_input[message.from_user.id] = False
        session = await db_connect.get_session()
        date_ = datetime.datetime.strptime(user_input, "%Y-%m-%d")
        res = await query_events_by_tg_id(
            session,
            message.from_user.id,
            date_
        )
        await message.answer(res)
    except ValueError:
        await message.answer("Такой даты несуществует. Введите дату корректно")
        return

@router_text.message(
    lambda message: waiting_for_input.get(message.from_user.id),
    F.text.regexp(
        "[0-9]{4}-(0[1-9]|1[012])-(0[1-9]|1[0-9]|2[0-9]|3[01])"))
def table_by_date_incorrect(message: types.Message):
    await message.answer("Ведите дату корректно")