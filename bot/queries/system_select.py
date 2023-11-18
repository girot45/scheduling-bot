
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.database import Table, User


async def list_of_users_for_notif_on_start(
        session: AsyncSession,
):
    stmt = (
        select(User.tgid)
        .filter(User.need_notif == 1))
    res = await session.execute(stmt)
    query = res.fetchall()
    await session.close()
    return query