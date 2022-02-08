from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp
from loader import dp
from utils.misc.logging import file_error_handler
import logging
from queue_commands import save_msg

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
logger.addHandler(file_error_handler)


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    await save_msg(message)
    text = ("I am queue_bot. ",
            "Use me for making a queue.")
    msg = await message.answer("\n".join(text))
    await save_msg(msg)
