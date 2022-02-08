from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Start"),
            types.BotCommand("help", "Info"),
            types.BotCommand("join_queue", "Get in line"),
            types.BotCommand("quit_queue", "Quit queue"),
            types.BotCommand("change_lab", "Change lab number"),
            types.BotCommand("show_number", "Show your number in queue"),
            types.BotCommand("show_history", "Show count of the people who left the queue."),
            types.BotCommand("delete_queue", "Delete current queue"),
            types.BotCommand('show_queue', 'Show queue'),
            types.BotCommand('remove_user', 'Remove user.'),
            types.BotCommand('next', 'Remove the first person in the queue.'),
            types.BotCommand('clear', 'Clear current session')
        ]
    )
