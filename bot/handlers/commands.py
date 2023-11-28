from aiogram import types, Router
from aiogram.filters import Command

from bot.database.db_manager import db_connect
from bot.handlers.buttons_manager import main_menu_buttons
from bot.queries.updates import update_user_schedule
from bot.queries.user_queries import check_user_in_db, insert_new_user
from bot.scheduler_manager import scheduler, \
    turn_of_schedule_for_user, turn_on_schedule_for_user

router_commands = Router()


@router_commands.message(Command("start"))
async def start(message: types.Message):
    session = await db_connect.get_session()
    tgid = message.from_user.id
    if not await check_user_in_db(
            session=session,
            tgid=tgid
    ):
        await insert_new_user(
            session=session,
            tgid=tgid,
            username=message.from_user.username
        )
        await message.answer(
            "Добро пожаловать!!! Этот бот поможет вам с расписанием."
            "Чтобы добавить событие отправьте боту сообщение в виде\n"
            "2024-01-01 00:00 (необязательно) Новый год"

        )

    await message.answer(
        "Меню",
        reply_markup=main_menu_buttons()
    )


@router_commands.message(Command("notif"))
async def switch_notif(message: types.Message):
    session = await db_connect.get_session()
    tgid = message.from_user.id
    job = scheduler.get_job(f"{tgid}ev")
    if job:
        await update_user_schedule(
            session=session,
            need_notif=0,
            tgid=tgid
        )
        turn_of_schedule_for_user(tgid)
        mes_to_user = "Уведомления отключены. Чтобы включить, " \
                      "введите /notif"
    else:
        await update_user_schedule(
            session=session,
            need_notif=1,
            tgid=tgid
        )
        turn_on_schedule_for_user(tgid)
        mes_to_user = "Уведомления включены. Чтобы выключить, " \
                      "введите /notif"
    await message.answer(mes_to_user)
