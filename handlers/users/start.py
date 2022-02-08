from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from utils.db_api.queue_db import save_msg_id
from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    if message.from_user.username is not None:
        text = f"Hi, @{message.from_user.username}!"
    else:
        text = f"Hi, {message.from_user.full_name}!"
    msg = await message.reply(text)
    await save_msg_id(msg.message_id)
