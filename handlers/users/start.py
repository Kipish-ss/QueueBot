from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from loader import dp
from utils.misc.logging import get_logger
from .queue_commands import save_msg

logger = get_logger()


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await save_msg(message)
    if message.from_user.username is not None:
        text = f"Hi, @{message.from_user.username}!"
    else:
        text = f"Hi, {message.from_user.full_name}!"
    msg = await message.reply(text)
    await save_msg(msg)
