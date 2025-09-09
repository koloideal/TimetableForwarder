from aiogram.types import Message


async def unknown_command(message: Message) -> None:
    await message.answer("unknown")
