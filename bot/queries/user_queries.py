from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.database import Table, User


async def check_user_in_db(
        session: AsyncSession,
        tgid: int,
):
    try:
        stmt = select(User.tgid).filter(User.tgid == tgid)
        res = await session.execute(stmt)
        query = res.fetchall()
        if query:
            return True
        else:
            return False

    except:
        return False


async def insert_new_user(
        session: AsyncSession,
        tgid: int,
        username: str
):
    try:
        new_user = User(
            tgid=int(tgid),
            username=username,
            need_notif=1
        )
        session.add(new_user)
        await session.commit()
        await session.close()
    except Exception as e:
        print(e)