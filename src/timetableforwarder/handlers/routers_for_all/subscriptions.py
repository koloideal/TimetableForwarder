from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from timetableforwarder.database.dao.users_dao import UsersDAO
from timetableforwarder.handlers.routers_for_all.rout_start import start_rout
from timetableforwarder.utils.get_config import Config, load_config


config: Config = load_config()

def _parse_selected(selected_str: str | None) -> set[int]:
    if not selected_str:
        return set()
    parts = [p for p in selected_str.split(":") if p]
    res: set[int] = set()
    for p in parts:
        if p.isdigit():
            res.add(int(p))
    return res


def _serialize_selected(selected: set[int]) -> str | None:
    if not selected:
        return None
    return ":".join(str(x) for x in sorted(selected))


def _build_groups_kb(selected: set[int], off_selected: bool) -> InlineKeyboardMarkup:
    rows = []
    groups = config.groups
    i = 0
    while i < len(groups):
        first = groups[i]
        first_suffix = " ✅" if first in selected and not off_selected else " ❌"
        first_btn = InlineKeyboardButton(text=f"{first}{first_suffix}", callback_data=f"cfg_group:{first}")
        if i + 1 < len(groups):
            second = groups[i + 1]
            second_suffix = " ✅" if second in selected and not off_selected else " ❌"
            second_btn = InlineKeyboardButton(text=f"{second}{second_suffix}", callback_data=f"cfg_group:{second}")
            rows.append([first_btn, second_btn])
            i += 2
        else:
            rows.append([first_btn])
            i += 1
    off_check = " ✅" if off_selected or not selected else ""
    rows.append([InlineKeyboardButton(text=f"🔕 Отключено{off_check}", callback_data="cfg_off")])
    rows.append([InlineKeyboardButton(text="⬅ Назад", callback_data="cfg_back")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


async def open_config(cb: CallbackQuery, users_dao: UsersDAO) -> None:
    user_id: int = cb.from_user.id
    user = await users_dao.get_user_by_id(user_id)
    selected_set = _parse_selected(user.subscribed_groups) if user else set()
    await cb.message.edit_text("Выберите группы, расписание которых вы хотите получать:")
    await cb.message.edit_reply_markup(reply_markup=_build_groups_kb(selected_set, off_selected=(not selected_set)))
    await cb.answer()


async def select_group(cb: CallbackQuery, users_dao: UsersDAO, group: int) -> None:
    user_id: int = cb.from_user.id
    user = await users_dao.get_user_by_id(user_id)
    selected_set = _parse_selected(user.subscribed_groups) if user else set()
    if group in selected_set:
        selected_set.remove(group)
        msg = "Группа убрана"
    else:
        selected_set.add(group)
        msg = "Группа выбрана"
    new_value = _serialize_selected(selected_set)
    if new_value == _serialize_selected(_parse_selected(user.subscribed_groups) if user else set()):
        await cb.answer("Без изменений")
        return
    await users_dao.update_user(user_id=user_id, subscribed_groups=new_value)
    await cb.message.edit_reply_markup(reply_markup=_build_groups_kb(selected_set, off_selected=(not selected_set)))
    await cb.answer(msg)


async def select_off(cb: CallbackQuery, users_dao: UsersDAO) -> None:
    user_id: int = cb.from_user.id
    user = await users_dao.get_user_by_id(user_id)
    selected_set = _parse_selected(user.subscribed_groups) if user else set()
    if not selected_set:
        await cb.answer("Уже отключено")
        return
    await users_dao.update_user(user_id=user_id, subscribed_groups=None)
    await cb.message.edit_reply_markup(reply_markup=_build_groups_kb(set(), off_selected=True))
    await cb.answer("Рассылка отключена")


async def go_back(cb: CallbackQuery, users_dao: UsersDAO) -> None:
    await start_rout(cb.message, users_dao, called_user=(cb.from_user.id, cb.from_user.username))
    await cb.answer()


