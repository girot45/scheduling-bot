import datetime

from sqlalchemy.exc import SQLAlchemyError
from bot.database.database import Table


async def insert_event(table, session):
    try:
        day_of_week = datetime.date.fromisoformat(
            table["date"]).weekday()
        date_ = datetime.datetime.strptime(table["date"],
                                           '%Y-%m-%d').date()
        new_event = Table(
            tgid=table["tg_id"],
            date=date_,
            timestart=table['time_start'],
            timeend=table['time_end'],
            event=table['event'],
            isrepeat=table['is_repeat'],
            day_of_week=str(day_of_week)
        )

        session.add(new_event)
        await session.commit()
        await session.close()

        return True
    except SQLAlchemyError:
        await session.rollback()
        return False
