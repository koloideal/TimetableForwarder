from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat, BotCommandScopeDefault

from timetableforwarder.utils.get_config import Config


async def set_commands(bot: Bot, config: Config):
    user_commands = [
        BotCommand(command="start", description="🚀 Начало работы"),
        BotCommand(command="help", description="ℹ️ Справка"),
    ]

    creator_commands = user_commands + [
        BotCommand(command="start", description="🚀 Начало работы"),
        BotCommand(command="help", description="ℹ️ Справка"),
        BotCommand(command="ban_user", description="🚫 Забанить пользователя"),
        BotCommand(command="unban_user", description="✅ Разбанить пользователя"),
        BotCommand(command="list_banned", description="📜 Список заблокированных"),
        BotCommand(command="list_all_users", description="👥 Список всех пользователей"),
    ]

    await bot.set_my_commands(
        commands=user_commands,
        scope=BotCommandScopeDefault()
    )

    await bot.set_my_commands(
        commands=creator_commands,
        scope=BotCommandScopeChat(chat_id=config.creator_id)
    )
