from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from timetableforwarder.database.dao.users_dao import UsersDAO
from timetableforwarder.utils.get_config import Config, load_config
from typing import Optional

config: Config = load_config()
creator_id: str = config.creator_id


async def start_rout(message: Message, users_dao: UsersDAO, called_user: Optional[tuple[int, str]] = None) -> None:
    if called_user:
        user_id = called_user[0]
        username = called_user[1]
        menu_func = message.edit_text
    else:
        user_id = message.from_user.id
        username = message.from_user.username
        menu_func = message.answer
        
    creator_case: bool = user_id == creator_id
    user_case: bool = user_id != creator_id

    if creator_case:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Настроить рассылку ⚙️", callback_data="cfg_open")]
            ]
        )
        await menu_func(
            "🎓 <b>Добро пожаловать, создатель!</b>\n\n"
            "Этот бот автоматически распознаёт расписание с картинок из канала колледжа "
            "и пересылает его в выбранные группы студентов.\n\n"
            "Используйте кнопку ниже для настройки рассылки по группам.\n\n"
            "<i>made by kolo</i>",
            reply_markup=keyboard,
            parse_mode='HTML'
        )
    elif user_case:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Настроить рассылку ⚙️", callback_data="cfg_open")]
            ]
        )
        await menu_func(
            "🎓 <b>Добро пожаловать!</b>\n\n"
            "Этот бот поможет вам получать актуальное расписание из канала колледжа "
            "прямо в ваш чат или группу.\n\n"
            "Выберите свою группу для получения персональных уведомлений о расписании.\n\n"
            "<i>made by kolo</i>",
            reply_markup=keyboard,
            parse_mode='HTML'
        )

    await users_dao.create_user(
        user_id=user_id,
        username=username
    )
