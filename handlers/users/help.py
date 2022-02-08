from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp
from utils.db_api.queue_db import save_msg_id
from loader import dp


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("I am queue_bot. ",
            "Use me for making a queue.")
    msg = await message.answer("\n".join(text))
    await save_msg_id(msg.message_id)
