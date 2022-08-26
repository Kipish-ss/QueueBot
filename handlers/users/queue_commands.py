from loader import dp
from aiogram import types
from utils.db_api.queue_db import add_user, find_max, is_present, get_number, update_queue, \
    remove_user, show_count, is_quit, update_num, get_user, get_priority, \
    display_queue, reset_quit, get_avg_quit_num, clear_stats, set_queue_id
from message_functions import save_msg, delete_message
from data.config import ADMINS
from loader import bot
from keyboards.inline.get_inline_keyboards import get_add_keyboard, get_lab_keyboard, get_stats_keyboard, \
    get_reset_stats_keyboard
from keyboards.inline.callbackdata import options_callback, lab_callback, stats_callback, reset_stats_callback
from utils.misc.logging import get_logger

logger = get_logger()


@dp.message_handler(commands=["join_queue"])
async def add_to_queue(message: types.Message):
    await save_msg(message)
    try:
        present = await is_present(message.from_user.id)
        if not present:
            if message.from_user.username is not None:
                user_name = message.from_user.username
            else:
                user_name = message.from_user.full_name
            try:
                choice_msg = await message.reply(text='Choose your Lab:', reply_markup=get_lab_keyboard(
                    user_id=message.from_user.id, user_name=user_name, message_id=message.message_id,
                    present=present))
                await save_msg(choice_msg)
            except ValueError:
                logger.error('Resulted callback data is too long!\nPerhaps the username is too long.')
                user_name = message.from_user.first_name
                choice_msg = await message.reply(text='Choose your Lab:', reply_markup=get_lab_keyboard(
                    user_id=message.from_user.id, user_name=user_name, message_id=message.message_id,
                    present=present))
                await save_msg(choice_msg)
        else:
            quit = await is_quit(message.from_user.id)
            priority = await get_priority(message.from_user.id)
            if quit:
                user_name = (message.from_user.username if message.from_user.username is not None
                             else message.from_user.full_name)
                await bot.send_message(int(ADMINS[0]), text=f"Add {user_name}?", reply_markup=get_add_keyboard(
                    message.from_user.id, user_name, message.chat.id, priority=priority))
                msg = await message.reply("You have quit the queue. Wait for @kirish_ss to add you or wait for a new "
                                          "queue.")
                await save_msg(msg)
            else:
                num = await get_number(message.from_user.id)
                msg = await message.reply(
                    f'You are already in the queue. Your number is {num}, your lab is {priority}.\nUse '
                    f'/quit_queue command when you finish your lab.')
                await save_msg(msg)
            await save_msg(message)
    except Exception as ex:
        logger.exception(ex)


@dp.message_handler(commands=["show_number"])
async def show_number(message: types.Message):
    try:
        await save_msg(message)
        present = await is_present(message.from_user.id)
        if present:
            quit = await is_quit(message.from_user.id)
            if not quit:
                num = await get_number(message.from_user.id)
                msg = await message.reply(f'Your current number in queue is {num}.\nUse /quit_queue command when you '
                                          f'finish your lab.')
            else:
                msg = await message.reply("You have quit the queue. Use /join_queue command.")
        else:
            msg = await message.reply("You are not in the queue yet. Use /join_queue command to join the queue.")
        await save_msg(msg)
    except Exception:
        logger.exception('An unexpected error occurred.')
        msg = await message.reply('An unexpected error occurred.')
        await save_msg(msg)


@dp.message_handler(commands=["quit_queue"])
async def leave_queue(message: types.Message):
    try:
        await save_msg(message)
        present = await is_present(message.from_user.id)
        if present:
            quit = await is_quit(message.from_user.id)
            if not quit:
                text = "You have been successfully removed from the queue.\n"
                num = await get_number(message.from_user.id)
                await update_queue(num)
                await remove_user(user_id=message.from_user.id)
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
                msg = await message.reply(text)
            else:
                msg = await message.reply(
                    "You have already quit the queue.\nIf you want to rejoin, use /join_queue command.")
        else:
            msg = await message.reply("You are not in the queue.")
        await save_msg(msg)
    except Exception:
        logger.exception('An unexpected error occurred.')
        msg = await message.reply('An unexpected error occurred.')
        await save_msg(msg)


@dp.message_handler(commands='show_queue')
async def show_queue(message: types.Message):
    try:
        await save_msg(message)
        queue = await display_queue()
        if queue is not None:
            text = ""
            for person, pr_num_tpl in queue.items():
                if pr_num_tpl[0] == 1:
                    text += f'{pr_num_tpl[0]}: @{person} with lab {pr_num_tpl[1]}\n'
                else:
                    text += f'{pr_num_tpl[0]}: {person} with lab {pr_num_tpl[1]}\n'
            msg = await message.reply(text)
        else:
            msg = await message.reply("The queue is empty.")
        await save_msg(msg)
    except Exception:
        logger.exception("An unexpected error occurred.")
        msg = await message.reply("An unexpected error occurred.")
        await save_msg(msg)


@dp.message_handler(commands=["show_history"])
async def show_queue_history(message: types.Message):
    try:
        await save_msg(message)
        count = await show_count()
        if count != 1:
            msg = await message.reply(f"{count} people have already left the queue.")
        else:
            msg = await message.reply(f"{count} person has already left the queue.")
        await save_msg(msg)
    except Exception:
        logger.exception('An unexpected error occurred.')


@dp.message_handler(commands=['change_lab'])
async def change_lab(message: types.Message):
    try:
        user_id = message.from_user.id
        present = await is_present(user_id)
        if present:
            quit = await is_quit(message.from_user.id)
            if not quit:
                user_name = (message.from_user.username if message.from_user.username is not None
                             else message.from_user.full_name)
                await message.reply(text='Choose your Lab:', reply_markup=get_lab_keyboard(
                    user_id=message.from_user.id, user_name=user_name,
                    message_id=message.message_id, present=present))
            else:
                msg = await message.reply('You have quit the queue. Use /join_queue command '
                                          'if you want to rejoin the queue.')
                await save_msg(msg)
                await save_msg(message)
        else:
            msg = await message.reply("You are not in the queue.\nUse /join_queue command to join the queue.")
            await save_msg(msg)
            await save_msg(message)
    except Exception:
        logger.exception('An unexpected error occurred.')
        msg = await message.reply('An unexpected error occurred.')
        await save_msg(msg)


@dp.message_handler(commands=['stats'])
async def show_stats(message: types.Message):
    await delete_message(message)
    try:
        await message.answer(text="Choose the option you need:", reply_markup=get_stats_keyboard(message.from_user.id))
    except Exception:
        logger.exception("An error occurred when trying to show stats keyboard")


@dp.callback_query_handler(options_callback.filter(action="add"))
async def approve_user(call: types.CallbackQuery, callback_data: dict):
    try:
        user_id = callback_data.get("user_id")
        user_name = callback_data.get("user_name")
        chat_id = callback_data.get("chat_id")
        priority = int(callback_data.get("priority"))
        num = find_max(priority=priority)
        await update_num(user_id=user_id, num=num, priority=priority)
        msg = await bot.send_message(chat_id, text=f'@{user_name} is {num} in the queue with lab {priority}.')
        await save_msg(msg)
        await reset_quit(user_id)
        await call.message.edit_reply_markup()
        await delete_message(message_id=call.message.message_id, chat_id=int(ADMINS[0]))
    except Exception:
        logger.exception("An error occurred when adding user to the queue")


@dp.callback_query_handler(options_callback.filter(action="reject"))
async def reject_user(call: types.CallbackQuery, callback_data: dict):
    try:
        user_name = callback_data.get("user_name")
        chat_id = callback_data.get("chat_id")
        await call.message.reply(f'@{user_name} has not been added to the queue.')
        msg = await bot.send_message(chat_id, text=f'@{user_name} has not been added to the queue.')
        await save_msg(msg)
        await delete_message(call.message)
    except Exception:
        logger.exception("An error occurred when rejecting user")


@dp.callback_query_handler(lab_callback.filter())
async def set_priority(call: types.CallbackQuery, callback_data: dict):
    try:
        user_id = int(callback_data.get("user_id"))
        if user_id == call.from_user.id:
            user_name = callback_data.get("user_name")
            priority = int(callback_data.get("pr_num"))
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
                    num = find_max(priority, user_id)
                    await update_num(user_id=user_id, num=num, priority=priority, change=True)
                else:
                    num = num_previous
            text = f"Yu are {num} in the queue with lab {priority}.\nUse /quit_queue command " \
                   f"when you finish your lab.\nUse /change_lab command to change your lab number."
            await bot.answer_callback_query(call.id, text=text, show_alert=True)
            await delete_message(call.message)
            await delete_message(chat_id=call.message.chat.id, message_id=message_id)
    except Exception:
        logger.exception("An error occurred when choosing labs")


@dp.callback_query_handler(stats_callback.filter(option="reset"))
async def reset_stats(call: types.CallbackQuery, callback_data: dict):
    try:
        user_id = callback_data.get("user_id")
        if call.from_user.id == int(user_id) and user_id in ADMINS:
            await call.message.edit_text("Are you sure you want to reset the stats?")
            await call.message.edit_reply_markup(get_reset_stats_keyboard(user_id))
    except Exception:
        logger.exception("An error occurred when getting reset_stats keyboard")


@dp.callback_query_handler(stats_callback.filter())
async def stats_options(call: types.CallbackQuery, callback_data: dict):
    try:
        option = callback_data.get("option")
        if option == "avg_quit_num":
            avg_quit = await get_avg_quit_num()
            await call.answer(text=f'{round(avg_quit)} people on average left the queue', show_alert=True)
        else:
            await delete_message(call.message)
    except Exception:
        logger.exception("An error occurred in stats_options")


@dp.callback_query_handler(reset_stats_callback.filter())
async def reset_stats(call: types.CallbackQuery, callback_data: dict):
    try:
        option = callback_data.get("option")
        user_id = callback_data.get('user_id')
        if call.from_user.id == int(user_id):
            if option != "back":
                if option == "yes":
                    await clear_stats()
                    await call.answer(text="The stats were successfully reset", show_alert=True)
                    await set_queue_id()
                await delete_message(call.message)
            else:
                await call.message.edit_text("Choose the option you need:")
                await call.message.edit_reply_markup(get_stats_keyboard(user_id))
    except Exception:
        logger.exception("An error occurred when trying to reset stats")




