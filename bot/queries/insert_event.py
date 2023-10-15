import datetime

from sqlalchemy.exc import SQLAlchemyError
from bot.database.database import Table


async def insert_event(table, session):
        try:
            day_of_week = datetime.date.fromisoformat(table["Date"]).weekday()
            new_event = Table(
                tgid=table["tg_id"],
                date=table['Date'],
                timestart=table['TimeStart'],
                timeend=table['TimeEnd'],
                event=table['Event'],
                isrepeat=table['IsRepeat'],
                day_of_week=day_of_week
            )

            session.add(new_event)
            await session.commit()
            await session.close()

            return True
        except SQLAlchemyError:
            await session.rollback()
            return False
