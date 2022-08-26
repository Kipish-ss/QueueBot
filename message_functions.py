from aiogram.utils.exceptions import MessageCantBeDeleted, MessageToDeleteNotFound

from loader import bot
from utils.db_api.queue_db import save_msg_id
from aiogram import types
from utils.misc.logging import get_logger

logger = get_logger(handle_info=False)


async def save_msg(message: types.Message):
    try:
        await save_msg_id(message.message_id, message.chat.id)
    except Exception as ex:
        logger.exception(ex)


async def delete_message(message: types.Message = None, message_id: int = 0, chat_id: int = 0):
    if message:
        msg_id = message.message_id
        chat_id = message.chat.id
    else:
        msg_id = message_id
        chat_id = chat_id
    try:
        await bot.delete_message(chat_id=chat_id, message_id=msg_id)
    except (MessageCantBeDeleted, MessageToDeleteNotFound):
        logger.exception(f"Message cannot be deleted.")
