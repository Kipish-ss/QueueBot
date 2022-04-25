from utils.db_api.queue_db import save_msg_id
from aiogram import types
from utils.misc.logging import get_logger

logger = get_logger(handle_info=False)


async def save_msg(message: types.Message):
    try:
        await save_msg_id(message.message_id, message.chat.id)
    except Exception as ex:
        logger.exception(ex)