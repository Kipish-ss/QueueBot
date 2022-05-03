from aiogram.utils.callback_data import CallbackData
options_callback = CallbackData("choose", "action", "user_id", "user_name", "chat_id", "priority")
lab_callback = CallbackData("priority", "pr_num", "user_id", "user_name", "message_id", "present")
save_queue_callback = CallbackData("save", "option", "user_id")
stats_callback = CallbackData("choose", "option", "user_id")
delete_queue_callback = CallbackData("delete", "option", "user_id")
reset_stats_callback = CallbackData("reset", "option", "user_id")
