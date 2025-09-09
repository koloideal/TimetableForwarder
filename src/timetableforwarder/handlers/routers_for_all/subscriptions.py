from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from timetableforwarder.database.dao.users_dao import UsersDAO
from timetableforwarder.utils.get_config import Config, load_config


config: Config = load_config()


def _build_groups_kb(selected: int | None) -> InlineKeyboardMarkup:
    rows = []
    groups = config.groups
    i = 0
    while i < len(groups):
        first = groups[i]
        first_check = " ✅" if selected == first else ""
        first_btn = InlineKeyboardButton(text=f"{first}{first_check}", callback_data=f"cfg_group:{first}")
        if i + 1 < len(groups):
            second = groups[i + 1]
            second_check = " ✅" if selected == second else ""
            second_btn = InlineKeyboardButton(text=f"{second}{second_check}", callback_data=f"cfg_group:{second}")
            rows.append([first_btn, second_btn])
            i += 2
        else:
            rows.append([first_btn])
            i += 1
    off_check = " ✅" if selected is None else ""
    rows.append([InlineKeyboardButton(text=f"Отключено{off_check}", callback_data="cfg_off")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


async def open_config(cb: CallbackQuery, users_dao: UsersDAO) -> None:
    user_id: int = cb.from_user.id
    user = await users_dao.get_user_by_id(user_id)
    selected = user.subscribed_group if user else None
    await cb.message.edit_text("Выберите группу, расписание которой вы хотите получать:")
    await cb.message.edit_reply_markup(reply_markup=_build_groups_kb(selected))
    await cb.answer()


async def select_group(cb: CallbackQuery, users_dao: UsersDAO, group: int) -> None:
    user_id: int = cb.from_user.id
    await users_dao.update_user(user_id=user_id, subscribed_group=group)
    await cb.message.edit_reply_markup(reply_markup=_build_groups_kb(group))
    await cb.answer("Группа выбрана")


async def select_off(cb: CallbackQuery, users_dao: UsersDAO) -> None:
    user_id: int = cb.from_user.id
    await users_dao.update_user(user_id=user_id, subscribed_group=None)
    await cb.message.edit_reply_markup(reply_markup=_build_groups_kb(None))
    await cb.answer("Рассылка отключена")


