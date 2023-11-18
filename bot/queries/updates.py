import datetime

from sqlalchemy import select, update
from sqlalchemy.exc import SQLAlchemyError
from bot.database.database import Table, User


async def update_user_schedule(session, need_notif: int, tgid: int):
    stmt = (
        update(User).where(User.tgid == tgid)
        .values(need_notif=need_notif)
    )

    await session.execute(stmt)
    await session.commit()
