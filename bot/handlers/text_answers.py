import datetime

from aiogram import types, F, Router

from bot.database.db_manager import db_connect
from bot.queries.select_today import query_events_by_tg_id

router_text = Router()

@router_text.message(F.text.lower().in_({"сегодня"}))
async def answer_message_today(message: types.Message):
    session = await db_connect.get_session()
    date_today = datetime.date.today()
    res = await query_events_by_tg_id(
        session,
        message.from_user.id,
        date_today
    )

    await message.answer(res)