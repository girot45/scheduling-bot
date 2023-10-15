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