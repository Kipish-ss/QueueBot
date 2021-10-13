from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Start"),
            types.BotCommand("help", "Info"),
            types.BotCommand("join_queue", "Get in line"),
            types.BotCommand("quit_queue", "Quit queue"),
            types.BotCommand("show_number", "Show your number in queue"),
            types.BotCommand("show_history", "Show count of the people who left the queue."),
            types.BotCommand("delete_queue", "Delete current queue"),
            # types.BotCommand("add_to_queue", "Add person to the queue.")
        ]
    )
