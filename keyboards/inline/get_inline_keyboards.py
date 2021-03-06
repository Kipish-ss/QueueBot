from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .callbackdata import options_callback, lab_callback, save_queue_callback, stats_callback, delete_queue_callback, \
    reset_stats_callback
from data.config import MIN_PRIORITY, MAX_PRIORITY


def get_add_keyboard(user_id: int, user_name: str, chat_id: int, priority: int):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.insert(InlineKeyboardButton(text="Approve", callback_data=options_callback.new(
                action="add", user_id=user_id, user_name=user_name, chat_id=chat_id, priority=priority)))
    keyboard.insert(InlineKeyboardButton(text="Reject", callback_data=options_callback.new(
                action="reject", user_id=user_id, user_name=user_name, chat_id=chat_id, priority=priority)))
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
    yes_no_keyboard = InlineKeyboardMarkup(row_width=2)
    yes_no_keyboard.insert(InlineKeyboardButton(text="Yes", callback_data=save_queue_callback.new(option="yes",
                                                                                                  user_id=user_id)))
    yes_no_keyboard.insert(InlineKeyboardButton(text="No", callback_data=save_queue_callback.new(option="no",
                                                                                                 user_id=user_id)))
    yes_no_keyboard.insert(InlineKeyboardButton(text="Back👈", callback_data=save_queue_callback.new(option="back",
                                                                                                    user_id=user_id)))

    return yes_no_keyboard


def get_stats_keyboard(user_id: int):
    stats_keyboard = InlineKeyboardMarkup(row_width=2)
    stats_keyboard.insert(InlineKeyboardButton(text="Average quit num", callback_data=stats_callback.new(
        option="avg_quit_num", user_id=user_id)))
    stats_keyboard.insert(InlineKeyboardButton(text="Reset stats", callback_data=stats_callback.new(option="reset",
                                                                                                    user_id=user_id)))
    stats_keyboard.insert(InlineKeyboardButton(text="Close❌", callback_data=stats_callback.new(option="close",
                                                                                               user_id=user_id)))
    return stats_keyboard


def get_delete_queue_keyboard(user_id: int):
    delete_keyboard = InlineKeyboardMarkup(row_width=2)
    delete_keyboard.insert(InlineKeyboardButton(text="✅", callback_data=delete_queue_callback.new(option="yes",
                                                                                                  user_id=user_id)))
    delete_keyboard.insert(InlineKeyboardButton(text="❌", callback_data=delete_queue_callback.new(option="no",
                                                                                                  user_id=user_id)))
    return delete_keyboard


def get_reset_stats_keyboard(user_id: int):
    reset_stats_keyboard = InlineKeyboardMarkup(row_width=2)
    reset_stats_keyboard.insert(InlineKeyboardButton(text="Yes", callback_data=reset_stats_callback.new(option="yes",
                                                                                                        user_id=user_id)))
    reset_stats_keyboard.insert(InlineKeyboardButton(text="No", callback_data=reset_stats_callback.new(option="no",
                                                                                                       user_id=user_id)))
    reset_stats_keyboard.insert(InlineKeyboardButton(text="Back👈", callback_data=reset_stats_callback.new(
        option="back", user_id=user_id)))
    return reset_stats_keyboard
