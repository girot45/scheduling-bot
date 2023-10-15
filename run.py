from asyncio import exceptions

import asyncio

from bot.bot_manager import dp, bot
from bot.handlers.commands import router_commands
from bot.handlers.text_answers import router_text

from log_manager import logger
from bot.scripts.add_event import add_event_router


dp.include_routers(router_commands, add_event_router, router_text)


async def main():
    await dp.start_polling(bot)


try:
    asyncio.run(main())
except Exception:
    import traceback
    logger.warning(traceback.format_exc())
