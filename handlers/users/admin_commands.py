from loader import dp, bot
from aiogram import types
from utils.db_api.queue_db import is_present, get_number, update_queue, remove_user, reset_queue, show_count, \
    is_quit, get_user, is_empty, get_messages, set_queue_info, set_queue_id, delete_queue_info
from data.config import ADMINS
from keyboards.inline.get_inline_keyboards import get_save_queue_keyboard, get_delete_queue_keyboard
from keyboards.inline.callbackdata import save_queue_callback, delete_queue_callback
from utils.misc.logging import get_logger
from message_functions import save_msg, delete_message
import datetime

logger = get_logger()


@dp.message_handler(commands=["delete_queue"])
async def delete_queue(message: types.Message):
    if str(message.from_user.id) in ADMINS:
        await delete_message(message)
        await message.answer(text="Are you sure you want to delete the queue?", reply_markup=get_delete_queue_keyboard(
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
                    await delete_message(message)
                else:
                    msg = await message.reply(f"@{user_name} is not in the queue.")
                    await delete_message(message)
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
                await delete_message(message)
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
                    await delete_message(message_id=msg_id, chat_id=message.chat.id)
        except Exception:
            logger.exception(f'An unexpected error occurred.')
    else:
        msg = await message.reply("You do not have rights to use this command.")
        await save_msg(message)
        await save_msg(msg)


@dp.callback_query_handler(delete_queue_callback.filter())
async def choose_delete_or_not(call: types.CallbackQuery, callback_data: dict):
    option = callback_data.get("option")
    user_id = int(callback_data.get("user_id"))
    if call.from_user.id == user_id:
        if option == "yes":
            await call.message.edit_text("Do you want to save info about this queue?")
            await call.message.edit_reply_markup(reply_markup=get_save_queue_keyboard(user_id))
        else:
            await delete_message(call.message)


@dp.callback_query_handler(save_queue_callback.filter(option="back"))
async def return_to_del_choice(call: types.CallbackQuery, callback_data: dict):
    user_id = int(callback_data.get("user_id"))
    if call.from_user.id == user_id:
        try:
            await call.message.edit_text("Are you sure you want to delete the queue?")
            await call.message.edit_reply_markup(reply_markup=get_delete_queue_keyboard(user_id))
        except Exception:
            logger.exception("An unexpected error occurred")


@dp.callback_query_handler(save_queue_callback.filter())
async def delete_queue(call: types.CallbackQuery, callback_data: dict):
    user_id = int(callback_data.get("user_id"))
    if call.from_user.id == user_id:
        try:
            text = ""
            option = callback_data.get("option")
            if option == "yes":
                quit_num = await show_count()
                current_date = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
                await set_queue_info(quit_num, current_date)
                text = "The info about the queue was saved.\n"
            elif option == "no":
                await delete_queue_info()
                text = "The info about the queue was not saved.\n"
            await reset_queue()
            await set_queue_id()
            await delete_message(call.message)
            text += "The queue was deleted."
            await call.answer(text, show_alert=True)
            await bot.send_message(chat_id=ADMINS[0], text=text)
        except Exception:
            logger.exception('An unexpected error occurred')
