from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.bot_manager import bot
from bot.database.db_manager import db_connect
from bot.handlers.text_answers import send_table_today_or_tomorrow
from bot.queries.system_select import list_of_users_for_notif_on_start


scheduler = AsyncIOScheduler(timezone="Europe/Moscow")


async def init_shedule_on_start():
    session = await db_connect.get_session()
    users = await list_of_users_for_notif_on_start(session)
    for user in users:
        turn_on_schedule_for_user(user[0])


def turn_on_schedule_for_user(
        tgid: int
):
    scheduler.add_job(
        send_table_today_or_tomorrow,
        'cron',
        id=f"{tgid}mo",
        day_of_week='mon-sun',
        hour=8,
        minute=36,
        kwargs={'message': bot, 'chat_id': tgid, 'istomorrow': False},
        max_instances=5)

    scheduler.add_job(
        send_table_today_or_tomorrow,
        'cron',
        id=f"{tgid}ev",
        day_of_week='mon-sun',
        hour=20,
        minute=30,
        kwargs={'message': bot, 'chat_id': tgid, 'istomorrow': True},
        max_instances=5)


def turn_of_schedule_for_user(tgid: int):
    scheduler.remove_job(job_id=f"{tgid}ev")
    scheduler.remove_job(job_id=f"{tgid}mo")


