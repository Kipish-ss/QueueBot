from data.config import CHAT, ADMINS, TEST_CHAT
from aiogram import Dispatcher
import time
from utils.misc.logging import file_info_handler, file_error_handler
import logging
from aiogram.utils.exceptions import BadRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(file_info_handler)
logger.addHandler(file_error_handler)


async def on_startup_notify(dp: Dispatcher):
    try:
            notification = await dp.bot.send_message(chat_id=TEST_CHAT, text="The queue bot is launched!")
            logger.info('The bot is launched!')
            try:
                await dp.bot.pin_chat_message(chat_id=TEST_CHAT, message_id=notification.message_id, disable_notification=False)
            except BadRequest as ex:
                logger.exception(ex)
            await dp.bot.send_message(chat_id=TEST_CHAT, text='Wait a minute before bot can handle your commands!')
            for i in range(60, 0, -1):
                if i != 60 and i % 15 == 0:
                    await dp.bot.send_message(chat_id=TEST_CHAT, text=f'{i} seconds left before the start of the queue!')
                if i in [1, 2, 3]:
                    await dp.bot.send_message(chat_id=TEST_CHAT, text=f'{i}')
                time.sleep(1)
            start_notification = await dp.bot.send_message(chat_id=TEST_CHAT, text='The queue has started!')
            try:
                await dp.bot.pin_chat_message(chat_id=TEST_CHAT, message_id=start_notification.message_id)
            except BadRequest as ex:
                logger.exception(ex)
            logger.info('The queue has started!')
    except Exception as ex:
        logger.exception(ex)
