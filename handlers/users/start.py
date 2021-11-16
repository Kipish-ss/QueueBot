from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    if message.from_user.username is not None:
        text = f"Hi, @{message.from_user.username}!"
    else:
        text = f"Hi, {message.from_user.full_name}!"
    await message.reply(text)
