from aiogram.types import Message


async def unknown_command(message: Message) -> None:
    await message.answer(
        "❓ <b>Неизвестная команда</b>\n\n"
        "Используйте /start для начала работы с ботом или /help для получения справки.",
        parse_mode="HTML"
    )
