from data.config import CHAT, TEST_CHAT
import logging
from aiogram import executor
from loader import dp
import handlers
from utils.notify import on_startup_notify
from utils.set_bot_commands import set_default_commands
from utils.misc.logging import file_error_handler
import asyncio

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
logger.addHandler(file_error_handler)


async def on_startup(dispatcher):
    try:
        await set_default_commands(dispatcher)
    except Exception:
        logger.exception('An unexpected error occured')


async def on_shutdown(dispatcher):
    try:
        await dp.bot.send_message(CHAT, text='Goodbye!')
    except Exception as ex:
        logger.exception(ex)

if __name__ == '__main__':
    try:
        asyncio.get_event_loop().run_until_complete(on_startup_notify(dp))
        executor.start_polling(dispatcher=dp, on_startup=on_startup, on_shutdown=on_shutdown, skip_updates=True)
    except TimeoutError as ex:
        logger.exception(ex)
    except Exception:
        logger.exception('An unexpected error occured')

