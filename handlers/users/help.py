from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp
from loader import dp
from utils.misc.logging import logger
import logging
from .queue_commands import save_msg


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    await save_msg(message)
    text = ("I am queue_bot. ",
            "Use me for making a queue.")
    msg = await message.answer("\n".join(text))
    await save_msg(msg)
