from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .callbackdata import options_callback, lab_callback, save_queue_callback
from data.config import MIN_PRIORITY, MAX_PRIORITY


def get_add_keyboard(user_id: int, user_name: str, chat_id: int, priority: int):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Approve", callback_data=options_callback.new(
                action="add", user_id=user_id, user_name=user_name, chat_id=chat_id, priority=priority)),
            InlineKeyboardButton(text="Reject", callback_data=options_callback.new(
                action="reject", user_id=user_id, user_name=user_name, chat_id=chat_id, priority=priority))
        ]])
    return keyboard


def get_lab_keyboard(user_id: int, user_name: str, message_id: int, present: bool):
    lab_choice = InlineKeyboardMarkup(row_width=3)
    for i in range(MIN_PRIORITY, MAX_PRIORITY + 1):
        lab_choice.insert(InlineKeyboardButton(text=f'Lab_{i}',
                                               callback_data=lab_callback.new(pr_num=i, user_id=user_id,
                                                                              user_name=user_name,
                                                                              message_id=message_id, present=present)))
    return lab_choice


def get_save_queue_keyboard(user_id: int):
    yes_no_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Yes", callback_data=save_queue_callback.new(option="yes", user_id=user_id)),
            InlineKeyboardButton(text="No", callback_data=save_queue_callback.new(option="no", user_id=user_id))
        ]
    ])
    return yes_no_keyboard
