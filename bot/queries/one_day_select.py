from datetime import  date

from sqlalchemy import select, cast, Date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import or_

from bot.database.database import Table
from bot.queries.utils import \
    formatting_a_day_schedule_for_sending_a_message


async def query_events_by_tg_id(
        session: AsyncSession,
        tg_id: int,
        date_: date
):
        date_str = date_.strftime("%Y-%m-%d")
        day_of_week = date_.weekday()
        stmt = (
            select(Table)
            .filter(
                Table.tgid == tg_id,
                or_(
                    Table.date == cast(date_, Date),
                    ((Table.date <= cast(date_, Date)) &
                     (Table.day_of_week == str(day_of_week)) &
                     (Table.isrepeat == 1))
                )
            )
            .order_by(Table.timestart.asc(), Table.timeend.asc())
        )

        res = await session.execute(stmt)
        query = res.scalars()
        await session.close()

        return formatting_a_day_schedule_for_sending_a_message(
            query,
            date_
        )
