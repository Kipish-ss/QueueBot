from loader import dp
from aiogram import types
from utils.db_api.queue_db import is_present, get_number, update_queue, remove_user, reset_queue, show_count, \
    is_quit, get_user, is_empty, get_messages, set_queue_info, set_queue_id, delete_queue_info
from data.config import ADMINS
from loader import bot
from keyboards.inline.options import get_save_queue_keyboard
from keyboards.inline.callbackdata import save_queue_callback
from aiogram.utils.exceptions import MessageCantBeDeleted
from utils.misc.logging import get_logger
from message_saver import save_msg
import datetime

logger = get_logger()


@dp.message_handler(commands=["delete_queue"])
async def delete_queue(message: types.Message):
    if str(message.from_user.id) in ADMINS:
        await message.reply(text="Do you want to save the info about this queue?", reply_markup=get_save_queue_keyboard(
            message.from_user.id))
    else:
        msg = await message.reply("You do not have rights to use this command.")
        await save_msg(msg)
    await save_msg(message)


@dp.message_handler(commands=['remove_user'])
async def delete_user(message: types.Message):
    if str(message.from_user.id) in ADMINS:
        try:
            if message.reply_to_message is not None:
                present = await is_present(message.reply_to_message.from_user.id)
                user_name = (message.reply_to_message.from_user.username
                             if message.reply_to_message.from_user.username is not None
                             else message.from_user.full_name)
                if present:
                    user_id = message.reply_to_message.from_user.id
                    quit = await is_quit(user_id)
                    if not quit:
                        num = await get_number(user_id)
                        await update_queue(num)
                        await remove_user(user_id)
                        text = f"@{user_name} has been successfully removed from the queue.\n"
                        first_name = await get_user(1)
                        if first_name is not None:
                            text += f"@{first_name} is next!"
                            second_name = await get_user(2)
                            if second_name is not None:
                                text += f"\n@{second_name} is after @{first_name}"
                            else:
                                text += "There is nobody else in the queue."
                        else:
                            text += "This is the end of the queue."
                        msg = await message.answer(text)
                    else:
                        msg = await message.reply(f"@{user_name} has already been "
                                                                   f"removed from the queue.")
                    try:
                        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
                    except MessageCantBeDeleted:
                        logger.exception('Message with /remove_user command cannot be deleted.')
                else:
                    msg = await message.reply(f"@{user_name} is not in the queue.")
                    try:
                        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
                    except Exception as ex:
                        logger.exception(ex)
            else:
                await save_msg(message)
                msg = await message.reply("This command must be sent as a reply.")
            await save_msg(msg)
        except Exception:
            logger.exception("An unexpected error occurred.")
            msg = await message.reply("An unexpected error occurred.")
            await save_msg(msg)
    else:
        msg = await message.reply("You do no have rights to use this command.")
        await save_msg(message)
        await save_msg(msg)


@dp.message_handler(commands=['next'])
async def remove_first(message: types.Message):
    if str(message.from_user.id) in ADMINS:
        try:
            empty = await is_empty()
            if not empty:
                user_name = await get_user(1)
                text = f'@{user_name} has been successfully removed from the queue.\n'
                await remove_user(num=1)
                await update_queue(num=1)
                first_name = await get_user(1)
                if first_name is not None:
                    text += f"@{first_name} is next!"
                    second_name = await get_user(2)
                    if second_name is not None:
                        text += f"\n@{second_name} is after @{first_name}"
                    else:
                        text += " There is nobody else in the queue."
                else:
                    text += "This is the end of the queue."
                msg = await message.answer(text)
                try:
                    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
                except MessageCantBeDeleted:
                    logger.error(f'Message with command /next cannot be deleted.')
            else:
                msg = await message.reply('The queue is empty.')
                await save_msg(message)
            await save_msg(msg)
        except Exception:
            logger.exception('An unexpected error occurred')
            msg = await message.reply('An unexpected error occurred')
            await save_msg(msg)
    else:
        msg = await message.reply("You do not have rights to use this command.")
        await save_msg(message)
        await save_msg(msg)


@dp.message_handler(commands=['clear'])
async def clear_messages(message: types.Message):
    if str(message.from_user.id) in ADMINS or message.from_user.id == message.chat.id:
        try:
            await save_msg(message)
            id_list = await get_messages(message.chat.id)
            if id_list:
                for msg_id in id_list:
                    try:
                        await bot.delete_message(message_id=msg_id, chat_id=message.chat.id)
                    except Exception:
                        logger.exception(f'Message cannot be deleted.')
        except Exception:
            logger.exception(f'An unexpected error occurred.')
    else:
        msg = await message.reply("You do not have rights to use this command.")
        await save_msg(message)
        await save_msg(msg)


@dp.callback_query_handler(save_queue_callback.filter())
async def delete_queue(call: types.CallbackQuery, callback_data: dict):
    user_id = int(callback_data.get("user_id"))
    if call.from_user.id == user_id:
        option = callback_data.get("option")
        if option == "yes":
            quit_num = await show_count()
            current_date = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
            await set_queue_info(quit_num, current_date)
            text = "The info about the queue was saved.\n"
        else:
            await delete_queue_info()
            text = "The info about the queue was not saved.\n"
        await reset_queue()
        await set_queue_id()
        chat_id = call.message.chat.id
        try:
            await bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
        except MessageCantBeDeleted:
            logger.error('Inline keyboard cannot be deleted.')
        text += "The queue was deleted."
        msg = await call.message.reply_to_message.reply(text)
        await save_msg(msg)
