import datetime

from sqlalchemy.exc import SQLAlchemyError
from bot.database.database import Table


async def insert_event(table, session):
    try:
        day_of_week = datetime.date.fromisoformat(
            table["Date"]).weekday()
        date_ = datetime.datetime.strptime(table["Date"],
                                           '%Y-%m-%d').date()
        new_event = Table(
            tgid=table["tg_id"],
            date=date_,
            timestart=table['TimeStart'],
            timeend=table['TimeEnd'],
            event=table['Event'],
            isrepeat=table['IsRepeat'],
            day_of_week=str(day_of_week)
        )

        session.add(new_event)
        await session.commit()
        await session.close()

        return True
    except SQLAlchemyError:
        await session.rollback()
        return False


async def insert_note(table, session):
    try:
        day_of_week = datetime.date.fromisoformat(
            table["Date"]).weekday()
        date_ = datetime.datetime.strptime(table["Date"],
                                           '%Y-%m-%d').date()
        if table["Timestart"]:
            timestart = table["Timestart"]
        else:
            timestart = None

        new_event = Table(
            tgid=table["tg_id"],
            date=date_,
            timestart= timestart,
            event=table['Event'],
            day_of_week=str(day_of_week)
        )

        session.add(new_event)

        await session.commit()

        await session.close()


        return True
    except SQLAlchemyError as e:
        print(e)
        await session.rollback()
        return False