from loader import dp
from aiogram import types
from utils.db_api.queue_operations import add_user, find_max, is_present, get_number, update_queue, remove_user, \
    reset_queue, show_count, is_quit, update_num, get_user, get_priority, display_queue, reset_quit
from data.config import ADMINS, CHAT
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
        await message.reply(text='Choose your Lab:', reply_markup=get_lab_keyboard(
            user_id=message.from_user.id, user_name=user_name, chat_id=message.chat.id, message_id=message.message_id,
        present=present))
    else:
        quit = await is_quit(message.from_user.id)
        priority = await get_priority(message.from_user.id)
        if quit:
            user_name = (message.from_user.username if message.from_user.username is not None
                         else message.from_user.full_name)
            await bot.send_message(int(ADMINS[0]), text=f"Add {user_name}?", reply_markup=get_add_keyboard(
                message.from_user.id, user_name, message.chat.id, priority=priority))
            await message.reply("You have quit the queue. Wait for @kirish_ss to add you or wait for a new queue.")
        else:
            num = await get_number(message.from_user.id)
            await message.reply(f'You are already in the queue. Your number is {num}, your lab is {priority}.\nUse '
                                f'/quit_queue command when you finish your lab.')


@dp.message_handler(commands=["show_number"])
async def show_number(message: types.Message):
    present = await is_present(message.from_user.id)
    if present:
        quit = await is_quit(message.from_user.id)
        if not quit:
            num = await get_number(message.from_user.id)
            await message.reply(f'Your current number in queue is {num}.\nUse /quit_queue command when you '
                                f'finish your lab.')
        else:
            await message.reply("You have quit the queue. Use /join_queue command.")
    else:
        await message.reply("You are not in the queue yet. Use /join_queue command to join the queue.")


@dp.message_handler(commands=["quit_queue"])
async def leave_queue(message: types.Message):
    present = await is_present(message.from_user.id)
    if present:
        quit = await is_quit(message.from_user.id)
        if not quit:
            num = await get_number(message.from_user.id)
            await update_queue(num)
            await remove_user(user_id=message.from_user.id)
            first_name = await get_user(1)
            second_name = await get_user(2)
            if first_name is not None:
                await message.answer(f"@{first_name} is next!")
                if second_name is not None:
                    await message.answer(f"@{second_name} is after @{first_name}")
                else:
                    await message.answer("There is nobody else in the queue.")
            else:
                await message.answer("This is the end of the queue.")
            await message.reply("You have been successfully removed from the queue.")
        else:
            await message.reply("You have already quit the queue.\nIf you want to rejoin, use /join_queue command.")
    else:
        await message.reply("You are not in the queue.")


@dp.message_handler(lambda message: str(message.from_user.id) in ADMINS, commands=['remove_user'])
async def delete_user(message: types.Message):
    try:
        if message.reply_to_message is not None:
            present = await is_present(message.reply_to_message.from_user.id)
            if present:
                user_id = message.reply_to_message.from_user.id
                quit = await is_quit(user_id)
                if not quit:
                    num = await get_number(user_id)
                    await update_queue(num)
                    await remove_user(user_id)
                    first_name = await get_user(1)
                    second_name = await get_user(2)
                    if first_name is not None:
                        await message.answer(f"@{first_name} is next!")
                        if second_name is not None:
                            await message.answer(f"@{second_name} is after @{first_name}")
                        else:
                            await message.answer("There is nobody else in the queue.")
                    else:
                        await message.answer("This is the end of the queue.")
                    user_name = (message.reply_to_message.from_user.username if message.reply_to_message.from_user.username
                                                                                is not None
                                 else message.from_user.full_name)
                    await message.reply_to_message.reply(f"@{user_name} has been "
                                                         f"successfully removed from the queue.")
                    await bot.delete_message(chat_id=CHAT, message_id=message.message_id)
                else:
                    await message.reply_to_message.reply("This user has already been removed from the queue.")
            else:
                await message.reply_to_message.reply("The user is not in the queue.")
                await bot.delete_message(chat_id=CHAT, message_id=message.message_id)
        else:
            await message.reply("This command must be sent as a reply.")
    except Exception as ex:
        print(ex)
        await message.reply("An unexpected error occurred.")


@dp.message_handler(commands='show_queue')
async def show_queue(message: types.Message):
    try:
        queue = await display_queue()
        if queue is not None:
            text = ""
            for person, pr_num_tpl in queue.items():
                if pr_num_tpl[0] == 1:
                    text += f'{pr_num_tpl[0]}: @{person} with lab {pr_num_tpl[1]}\n'
                else:
                    text += f'{pr_num_tpl[0]}: {person} with lab {pr_num_tpl[1]}\n'
            await message.reply(text)
        else:
            await message.reply("The queue is empty.")
    except Exception as ex:
        print(ex)
        await message.reply("An unexpected error occurred.")


@dp.message_handler(commands=["show_history"])
async def show_queue_history(message: types.Message):
    count = await show_count()
    if count != 1:
        await message.reply(f"{count} people have already left the queue.")
    else:
        await message.reply(f"{count} person has already left the queue.")


@dp.message_handler(commands=['change_lab'])
async def change_lab(message: types.Message):
    user_id = message.from_user.id
    present = await is_present(user_id)
    if present:
        quit = await is_quit(message.from_user.id)
        if not quit:
            user_name = (message.from_user.username if message.from_user.username is not None
                         else message.from_user.full_name)
            await message.reply(text='Choose your Lab:', reply_markup=get_lab_keyboard(
                user_id=message.from_user.id, user_name=user_name, chat_id=message.chat.id,
                message_id=message.message_id, present=present))
        else:
            pass
    else:
        await message.reply("You are not in the queue.\nUse /join_queue command to join the queue.")


@dp.callback_query_handler(options_callback.filter(action="add"))
async def approve_user(call: types.CallbackQuery, callback_data: dict):
    user_id = callback_data.get("user_id")
    user_name = callback_data.get("user_name")
    chat_id = callback_data.get("chat_id")
    priority = int(callback_data.get("priority"))
    num = find_max(priority=priority)
    await update_num(user_id=user_id, num=num, priority=priority)
    await bot.send_message(chat_id, text=f'@{user_name} is {num} in the queue with lab {priority}.')
    await reset_quit(user_id)
    await call.message.edit_reply_markup()
    await bot.delete_message(message_id=call.message.message_id, chat_id=int(ADMINS[0]))


@dp.callback_query_handler(options_callback.filter(action="reject"))
async def reject_user(call: types.CallbackQuery, callback_data: dict):
    user_name = callback_data.get("user_name")
    chat_id = callback_data.get("chat_id")
    await call.message.reply(f'@{user_name} has not been added to the queue.')
    await bot.send_message(chat_id, text=f'@{user_name} has not been added to the queue.')
    await call.message.edit_reply_markup()


@dp.callback_query_handler(lab_callback.filter())
async def set_priority(call: types.CallbackQuery, callback_data: dict):
    user_id = int(callback_data.get("user_id"))
    if user_id == call.from_user.id:
        user_name = callback_data.get("user_name")
        priority = int(callback_data.get("pr_num"))
        chat_id = int(callback_data.get("chat_id"))
        message_id = int(callback_data.get("message_id"))
        present = callback_data.get("present")
        if present == 'False':
            num = find_max(priority=priority)
            await add_user(user_id=user_id, user_name=user_name, priority=priority, number=num)
        else:
            priority_previous = await get_priority(user_id)
            num_previous = await get_number(user_id)
            if priority != priority_previous:
                await update_queue(num_previous)
                num = find_max(priority)
                await update_num(user_id=user_id, num=num, priority=priority, change=True)
            else:
                num = num_previous
        await call.message.answer(f"@{user_name} is {num} in the queue with lab {priority}.\nUse /quit_queue commnad "
                                  f"when you finish your lab.\nUse /change_lab command to change your lab number.")
        try:
            await bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
            await bot.delete_message(message_id=message_id, chat_id=chat_id)
        except:
            print('Cannot delete')