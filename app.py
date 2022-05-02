from data.config import CHAT, TEST_CHAT
from aiogram import executor
from loader import dp
from utils.notify import on_startup_notify
import handlers
from utils.set_bot_commands import set_default_commands
from utils.misc.logging import get_logger
from utils.db_api.queue_db import set_queue_id, is_deleted
import asyncio

logger = get_logger()


async def on_startup(dispatcher):
    try:
        is_queue_deleted = await is_deleted()
        if is_queue_deleted:
            await set_queue_id()
        await set_default_commands(dispatcher)
    except Exception:
        logger.exception('An unexpected error occurred')


async def on_shutdown(dispatcher):
    try:
        await dp.bot.send_message(CHAT, text='Goodbye!')
    except Exception as ex:
        logger.exception(ex)


if __name__ == '__main__':
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(on_startup_notify(dp))
        executor.start_polling(dispatcher=dp, on_startup=on_startup, on_shutdown=on_shutdown, skip_updates=True,
                               timeout=0.1)
    except TimeoutError as ex:
        logger.exception(ex)
    except Exception:
        logger.exception('An unexpected error occurred')
