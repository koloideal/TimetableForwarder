from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from timetableforwarder.utils.get_config import load_config, Config
from timetableforwarder.utils.config_editor import remove_group
from timetableforwarder.handlers.routers_for_all.rout_start import start_rout
from timetableforwarder.database.dao.users_dao import UsersDAO


config: Config = load_config()


def _kb_groups_for_delete() -> InlineKeyboardMarkup:
    rows = []
    groups = load_config().groups
    i = 0
    while i < len(groups):
        first = groups[i]
        first_btn = InlineKeyboardButton(text=f"📘 {first}", callback_data=f"del_grp:{first}")
        if i + 1 < len(groups):
            second = groups[i + 1]
            second_btn = InlineKeyboardButton(text=f"📘 {second}", callback_data=f"del_grp:{second}")
            rows.append([first_btn, second_btn])
            i += 2
        else:
            rows.append([first_btn])
            i += 1
    rows.append([InlineKeyboardButton(text="⬅ Назад", callback_data="del_back")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def _kb_confirm(group: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Да", callback_data=f"del_yes:{group}"),
                InlineKeyboardButton(text="❌ Нет", callback_data="del_no"),
            ]
        ]
    )


def _kb_return() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="↩ Вернуться", callback_data="del_return")]])


async def del_group_entry(message: Message) -> None:
    await message.answer("Какую группу хотите удалить?", reply_markup=_kb_groups_for_delete())


async def del_group_select(cb: CallbackQuery, group: int) -> None:
    await cb.message.edit_text(f"Точно хотите удалить группу <b>{group}</b>?", parse_mode='HTML')
    await cb.message.edit_reply_markup(reply_markup=_kb_confirm(group))
    await cb.answer()


async def del_group_yes(cb: CallbackQuery, group: int, users_dao: UsersDAO) -> None:
    users = await users_dao.get_all_users()
    for user in users:
        subs = user.subscribed_groups or ""
        parts = [p for p in subs.split(":") if p]
        filtered = ":".join(p for p in parts if p != str(group)) or None
        if filtered != subs:
            await users_dao.update_user(user_id=user.user_id, subscribed_groups=filtered)
    ok = remove_group(group)
    if ok:
        await cb.message.edit_text(f"Успешно удалена группа <b>{group}</b>", parse_mode='HTML')
    else:
        await cb.message.edit_text(f"Группа <b>{group}</b> не найдена", parse_mode='HTML')
    await cb.message.edit_reply_markup(reply_markup=_kb_return())
    await cb.answer()


async def del_group_no(cb: CallbackQuery) -> None:
    await cb.message.edit_text("Какую группу хотите удалить?", parse_mode='HTML')
    await cb.message.edit_reply_markup(reply_markup=_kb_groups_for_delete())
    await cb.answer()


async def del_group_back(cb: CallbackQuery, users_dao: UsersDAO) -> None:
    await start_rout(cb.message, users_dao, called_user=(cb.from_user.id, cb.from_user.username))
    await cb.answer()


