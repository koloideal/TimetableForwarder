from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from timetableforwarder.database.dao.users_dao import UsersDAO
from timetableforwarder.utils.get_config import Config, load_config

config: Config = load_config()
creator_id: str = config.creator_id


async def start_rout(message: Message, users_dao: UsersDAO) -> None:
    username: str = message.from_user.username
    user_id: int = message.from_user.id

    creator_case: bool = user_id == creator_id
    user_case: bool = user_id != creator_id

    if creator_case:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Настроить рассылку", callback_data="cfg_open")]
            ]
        )
        await message.answer(
            "🎓 <b>Добро пожаловать, создатель!</b>\n\n"
            "Этот бот автоматически распознаёт расписание с картинок из канала колледжа "
            "и пересылает его в выбранные группы студентов.\n\n"
            "Используйте кнопку ниже для настройки рассылки по группам.",
            reply_markup=keyboard,
            parse_mode='HTML'
        )
    elif user_case:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Настроить рассылку ⚙️", callback_data="cfg_open")]
            ]
        )
        await message.answer(
            "🎓 <b>Добро пожаловать!</b>\n\n"
            "Этот бот поможет вам получать актуальное расписание из канала колледжа "
            "прямо в ваш чат или группу.\n\n"
            "Выберите свою группу для получения персональных уведомлений о расписании.",
            reply_markup=keyboard,
            parse_mode='HTML'
        )

    await users_dao.create_user(
        user_id=user_id,
        username=username
    )
