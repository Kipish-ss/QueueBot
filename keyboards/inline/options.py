from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .callbackdata import options_callback, lab_callback
from data.config import min_priority


def get_add_keyboard(user_id: int, user_name: str, chat_id: int):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Approve", callback_data=options_callback.new(action="add", user_id=user_id, user_name=user_name, chat_id=chat_id)),
            InlineKeyboardButton(text="Reject", callback_data=options_callback.new(action="reject", user_id=user_id, user_name=user_name, chat_id=chat_id))
        ]])
    return keyboard


def get_lab_keyboard(user_id: int, user_name: str, chat_id: int):
    lab_choice = InlineKeyboardMarkup(row_width=3)
    for i in range(min_priority, 10):
        lab_choice.insert(InlineKeyboardButton(text=f'Lab_{i}', callback_data=lab_callback.new(pr_num=i, user_id=user_id, user_name=user_name, chat_id=chat_id)))
    return lab_choice
