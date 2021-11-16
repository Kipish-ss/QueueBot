import time
import logging
from aiogram import executor
from loader import dp
import handlers
from utils.notify import on_startup_notify
from utils.set_bot_commands import set_default_commands
from data.config import CHAT
from utils.misc.logging import file_error_handler
import asyncio


logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
logger.addHandler(file_error_handler)


async def countdown():
    try:
        await dp.stop_polling()
        for i in range(60, 0, -1):
            if i != 60 and i % 15 == 0:
                await dp.bot.send_message(chat_id=CHAT, text=f'{i} seconds left before the start of the queue!')
            if i in [1, 2, 3]:
                await dp.bot.send_message(chat_id=CHAT, text=f'{i}')
            time.sleep(1)
        notification = await dp.bot.send_message(chat_id=CHAT, text='The queue has started!')
        await dp.bot.pin_chat_message(chat_id=CHAT, message_id=notification.message_id)
        executor.start_polling(dispatcher=dp, on_startup=on_startup, skip_updates=True)
    except Exception:
        logger.exception('An unexpected error occured')


async def on_startup(dispatcher):
    await set_default_commands(dispatcher)
    # await countdown()
    # await on_startup_notify(dispatcher)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(on_startup_notify(dp))
    executor.start_polling(dispatcher=dp, on_startup=on_startup, skip_updates=True)

