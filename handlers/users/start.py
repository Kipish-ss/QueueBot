from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from loader import dp
from utils.misc.logging import file_error_handler
import logging
from .queue_commands import save_msg

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
logger.addHandler(file_error_handler)


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await save_msg(message)
    if message.from_user.username is not None:
        text = f"Hi, @{message.from_user.username}!"
    else:
        text = f"Hi, {message.from_user.full_name}!"
    msg = await message.reply(text)
    await save_msg(msg)
