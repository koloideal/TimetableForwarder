from aiogram.types import Message


async def help_rout(message: Message) -> None:
    await message.answer(
        "Help command",
        parse_mode="HTML",
        disable_web_page_preview=True,
    )
