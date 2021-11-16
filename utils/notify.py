import logging
from data.config import CHAT
from aiogram import Dispatcher
from data.config import ADMINS
import time


async def on_startup_notify(dp: Dispatcher):
        try:
            notification = await dp.bot.send_message(chat_id=CHAT, text="The queue bot is launched!")
            await dp.bot.pin_chat_message(chat_id=CHAT, message_id=notification.message_id, disable_notification=False)
            await dp.bot.send_message(chat_id=CHAT, text='Wait a minute before bot can handle your commands!')
            for i in range(60, 0, -1):
                if i != 60 and i % 15 == 0:
                    await dp.bot.send_message(chat_id=CHAT, text=f'{i} seconds left before the start of the queue!')
                if i in [1, 2, 3]:
                    await dp.bot.send_message(chat_id=CHAT, text=f'{i}')
                time.sleep(1)
            start_notification = await dp.bot.send_message(chat_id=CHAT, text='The queue has started!')
            await dp.bot.pin_chat_message(chat_id=CHAT, message_id=start_notification.message_id)
        except Exception as err:
            logging.exception(err)
