import time
from datetime import datetime

from aiogram import types, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot.States import AddEventStates, DeleteEventStates
from bot.database.db_manager import db_connect
from bot.handlers.buttons_manager import (
    yes_or_no_buttons,
    approve_buttons,
    main_menu_buttons,
    dont_need_button
)
from bot.messages.messages_texts import *
from bot.queries.insert_event import insert_event

delete_event_router = Router()


@delete_event_router.message(Command("delete_event"))
async def delete_event(message: types.Message, state: FSMContext):
    await message.answer(f"{DELETE_EVENT_MES}")
    await message.answer(f"{DATE_OR_WEEKDAY_MES}")
    await state.set_state(DeleteEventStates.date_or_weekday)

@delete_event_router.message(
    DeleteEventStates.date_or_weekday,
    F.text.lower().in_({"по дате"})
)
async def choose_filter_type_for_delete(
        message: types.Message,
        state: FSMContext
):
    await state.update_data(date_or_weekday=1)
    await message.answer(WRITE_DATE_MES)
    await state.set_state(DeleteEventStates.date)


@delete_event_router.message(
    DeleteEventStates.date_or_weekday,
    F.text.lower().in_({"по дню недели"})
)
async def choose_filter_type_for_delete(
        message: types.Message,
        state: FSMContext
):
    await state.update_data(date_or_weekday=0)
    await message.answer(WRITE_DATE_MES)
    await state.set_state(DeleteEventStates.weekday)


@delete_event_router.message(
    DeleteEventStates.date,
    F.text.regexp(
        "[0-9]{4}-(0[1-9]|1[012])-(0[1-9]|1[0-9]|2[0-9]|3[01])")
)
async def enter_date_to_delete_event(
        message: types.Message,
        state: FSMContext
):
    await message.anwser("Вот все события на эту дату")
