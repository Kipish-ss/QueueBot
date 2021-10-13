from loader import dp
from aiogram import types
from utils.db_api.queue_operations import add_user, find_max, is_present, get_number, update_queue, remove_user, reset_queue, show_count, is_quit, update_num, reset_quit, get_user
from data.config import ADMINS
from loader import bot
from keyboards.inline.options import get_add_keyboard, get_lab_keyboard
from keyboards.inline.callbackdata import options_callback, lab_callback


@dp.message_handler(lambda message: str(message.from_user.id) in ADMINS, commands=["delete_queue"])
async def delete_queue(message: types.Message):
    await reset_queue()
    await message.reply("The queue was deleted.")


@dp.message_handler(commands=["join_queue"])
async def add_to_queue(message: types.Message):
    present = await is_present(message.from_user.id)
    if not present:
        if message.from_user.username is not None:
            user_name = message.from_user.username
        else:
            user_name = message.from_user.full_name
        await message.reply(text='Choose your Lab:', reply_markup=get_lab_keyboard(user_id=message.from_user.id, user_name=user_name, chat_id=message.chat.id))

    else:
        quit = await is_quit(message.from_user.id)
        if quit:
            user_name = (message.from_user.username if message.from_user.username is not None else message.from_user.full_name)
            await bot.send_message(int(ADMINS[0]), text=f"Add {user_name}?", reply_markup=get_add_keyboard(message.from_user.id, user_name, message.chat.id))
            await message.reply("You have quit the queue. Wait for @kirish_ss to add you or wait for a new queue.")
        else:
            num = await get_number(message.from_user.id)
            await message.reply(f'You are already in the queue. Your number is {num}.')


@dp.message_handler(commands=["show_number"])
async def show_number(message: types.Message):
    present = await is_present(message.from_user.id)
    if present:
        quit = await is_quit(message.from_user.id)
        if not quit:
            num = await get_number(message.from_user.id)
            await message.reply(f'Your current number in queue is {num}')
        else:
            await message.reply("You have quit the queue. Use /join_queue command.")
    else:
        await message.reply("You are not in the queue yet. Use /join_queue command to join the queue.")


@dp.message_handler(commands=["quit_queue"])
async def leave_queue(message: types.Message):
    num = await get_number(message.from_user.id)
    await update_queue(num)
    await remove_user(user_id=message.from_user.id)
    fist_name = await get_user(1)
    second_name = await get_user(2)
    await message.answer(f"@{fist_name} is now!")
    await message.answer(f"@{second_name} is next!")
    await message.reply("You have been successfully removed from the queue.")


@dp.message_handler(commands=["show_history"])
async def show_queue_history(message: types.Message):
    count = await show_count()
    if count != 1:
        await message.reply(f"{count} people have already left the queue.")
    else:
        await message.reply(f"{count} person has already left the queue.")


@dp.callback_query_handler(options_callback.filter(action="add"))
async def approve_user(call: types.CallbackQuery, callback_data: dict):
    user_id = callback_data.get("user_id")
    user_name = callback_data.get("user_name")
    chat_id = callback_data.get("chat_id")
    num = await find_max()
    await update_num(user_id, num)
    await reset_quit(user_id)
    await call.message.reply(f'@{user_name} has been successfully added to the queue.')
    await bot.send_message(chat_id=chat_id, text=f'@{user_name} has been successfully added to the queue.')
    await call.message.edit_reply_markup()


@dp.callback_query_handler(options_callback.filter(action="reject"))
async def reject_user(call: types.CallbackQuery, callback_data: dict):
    user_name = callback_data.get("user_name")
    chat_id = callback_data.get("chat_id")
    await call.message.reply(f'@{user_name} has not been added to the queue.')
    await bot.send_message(chat_id, text=f'@{user_name} has not been added to the queue.')
    await call.message.edit_reply_markup()


@dp.callback_query_handler(lab_callback.filter())
async def set_priority(call: types.CallbackQuery, callback_data: dict):
    user_name = (callback_data.get("user_name"))
    user_id = int(callback_data.get("user_id"))
    priority = int(callback_data.get("pr_num"))
    chat_id = int(callback_data.get("chat_id"))
    num = await find_max(priority=priority)
    await add_user(user_id=user_id, user_name=user_name, priority=priority, number=num)
    await call.message.answer(f"@{user_name} is {num} in the queue.")
    await bot.delete_message(message_id=call.message.message_id, chat_id=chat_id)