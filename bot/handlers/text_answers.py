from datetime import date, timedelta, datetime
import re
from typing import Optional

from aiogram import types, F, Router, Bot
from aiogram.fsm.context import FSMContext

from bot.States import TableDate
from bot.database.db_manager import db_connect
from bot.handlers.buttons_manager import main_menu_buttons
from bot.messages.formating_messages import \
    formatting_a_day_schedule_for_sending_a_message
from bot.messages.messages_texts import WRITE_DATE_MES, \
    WRITE_EVENT_TO_DB_MES, WRITE_EVENT_TO_DB_SUCCESS_MES, \
    WRITE_EVENT_TO_DB_ERROR_MES
from bot.queries.insert_event import insert_note
from bot.queries.one_day_select import query_events_by_tg_id

router_text = Router()


@router_text.message(F.text.lower().in_({"сегодня", "завтра"}))
async def send_table_today_or_tomorrow(
        message: Optional[Bot | types.Message],
        chat_id: Optional[int] = None,
        istomorrow: Optional[bool] = None,
):
    session = await db_connect.get_session()
    date_ = date.today()
    message_type = type(message)
    if message_type == types.Message:
        send_id = message.from_user.id
    else:
        send_id = chat_id
    if (message_type == types.Message and
        message.text.lower() == "завтра") or istomorrow:
        date_ += timedelta(days=1)

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


@router_text.message(F.text.in_({"Выбрать дату"}))
async def send_message_on_date(
        message: types.Message,
        state: FSMContext
):
    await message.answer(WRITE_DATE_MES)
    await state.set_state(TableDate.Date)


@router_text.message(
    TableDate.Date,
    F.text.regexp(
        "[0-9]{4}-(0[1-9]|1[012])-(0[1-9]|1[0-9]|2[0-9]|3[01])")
)
async def input_received(
        message: types.Message,
        state: FSMContext
):
    user_input = message.text
    try:

        if date.fromisoformat(user_input):
            pass
        await message.answer(f"Вы ввели: {user_input}")
        session = await db_connect.get_session()

        date_ = datetime.fromisoformat(user_input)
        res = await query_events_by_tg_id(
            session,
            message.from_user.id,
            date_
        )
        mes_to_user = \
            formatting_a_day_schedule_for_sending_a_message(
                res,
                date_
            )
        await message.answer(mes_to_user)
        await state.clear()
    except ValueError:
        await message.answer(
            "Такой даты несуществует. Введите дату корректно")
        return


@router_text.message(F.text)
async def fast_add_note(message: types.Message, ):
    try:
        message_text_source = message.text.split(" ")
        if len(message_text_source) == 1:
            await message.answer(
                "Вы можете сделать быстрое добавление события если "
                "введете сообщение \nДАТА\nВРЕМЯ НАЧАЛА\n СОБЫТИЕ. \n"
                "Пример сообщения\n\n 2024-01-01 "
                "00:00(это необязательно) Новый год"
            )
            return
        date_of_note = message_text_source[0]

        if not re.match(
                r"[0-9]{4}-(0[1-9]|1[012])-(0[1-9]|1[0-9]|2[0-9]|3[01])",
                date_of_note
        ):
            await message.answer(
                "Вы можете сделать быстрое добавление события если "
                "введете сообщение \nДАТА\nВРЕМЯ НАЧАЛА\n СОБЫТИЕ. \n"
                "Пример сообщения\n\n 2024-01-01 "
                "00:00(это необязательно) Новый год"
            )
            return

        if re.match(
                r"^([01]?[0-9]|2[0-3]):[0-5][0-9]$",
                message_text_source[1]
        ):
            timestart = message_text_source[1]
            text_of_note = ' '.join(message_text_source[2::])
        else:
            timestart = ""
            text_of_note = ' '.join(message_text_source[1::])

        if date.fromisoformat(date_of_note):
            pass
        data_to_db = {
            "tg_id": message.from_user.id,
            "Date": date_of_note,
            "Timestart": timestart,
            "Event": text_of_note,
        }

        await message.answer(WRITE_EVENT_TO_DB_MES)
        session = await db_connect.get_session()
        res = await insert_note(data_to_db, session)
        if res:
            answer_str = WRITE_EVENT_TO_DB_SUCCESS_MES
        else:
            answer_str = WRITE_EVENT_TO_DB_ERROR_MES
        await message.answer(answer_str)
        await message.answer("Меню",
                             reply_markup=main_menu_buttons())
    except ValueError:
        await message.answer(
            "Дата введена некорректно"
        )
    except:
        await message.answer(
            "Вы можете сделать быстрое добавление события если "
            "введете сообщение \nДАТА\nВРЕМЯ НАЧАЛА ("
            "необязательно)\n СОБЫТИЕ. \n"
            "Пример сообщения\n\n "
            "2024-01-01 00:00(это необязательно) Новый год"
        )
