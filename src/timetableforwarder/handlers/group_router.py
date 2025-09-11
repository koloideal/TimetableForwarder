from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.enums.chat_type import ChatType
from dishka.integrations.aiogram import FromDishka

from timetableforwarder.middlewares.is_admin_in_group_filter import IsAdminFilter 
from timetableforwarder.database.dao.subscribed_groups_dao import SubscribedGroupsDAO
from timetableforwarder.utils.get_config import Config
from typing import Optional


group_router = Router()
group_router.message.filter(F.chat.type.in_({ChatType.GROUP, ChatType.SUPERGROUP}))
group_router.callback_query.filter(F.message.chat.type.in_({ChatType.GROUP, ChatType.SUPERGROUP}))


def _build_groups_kb_single_choice(config: Config, current_selected: Optional[int]) -> InlineKeyboardMarkup:
    rows = []
    groups = config.groups
    i = 0
    while i < len(groups):
        first = groups[i]
        first_suffix = " ✅" if current_selected == first else ""
        first_btn = InlineKeyboardButton(text=f"🎓 {first}{first_suffix}", callback_data=f"grp_set:{first}")
        if i + 1 < len(groups):
            second = groups[i + 1]
            second_suffix = " ✅" if current_selected == second else ""
            second_btn = InlineKeyboardButton(text=f"🎓 {second}{second_suffix}", callback_data=f"grp_set:{second}")
            rows.append([first_btn, second_btn])
            i += 2
        else:
            rows.append([first_btn])
            i += 1
    off_suffix = " ✅" if current_selected is None else ""
    rows.append([InlineKeyboardButton(text=f"🔕 Отключено{off_suffix}", callback_data="grp_off")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


@group_router.message(
    Command("set_group"),
    IsAdminFilter()
)
async def set_group_handler(message: Message, subscribed_groups_dao: FromDishka[SubscribedGroupsDAO], config: FromDishka[Config]) -> None:
    current_group_model = await subscribed_groups_dao.get_group_by_telegram_id(message.chat.id)
    current_selected: Optional[int] = current_group_model.subscribed_group if current_group_model and current_group_model.subscribed_group else None

    if current_selected is not None:
        result_text = f"<i>Выберите группу для пересылки расписания, текущая группа <b>{current_selected}</b>:</i>"
    else:
        result_text = "<i>Выберите группу для пересылки расписания:</i>"

    await message.reply(
        result_text,
        reply_markup=_build_groups_kb_single_choice(config, current_selected)
    )


@group_router.callback_query(F.data.startswith("grp_set:"))
async def set_group_callback(cb: CallbackQuery, subscribed_groups_dao: FromDishka[SubscribedGroupsDAO]) -> None:
    member = await cb.message.bot.get_chat_member(
        chat_id=cb.message.chat.id,
        user_id=cb.from_user.id
    )
    if member.status not in ("administrator", "creator"):
        await cb.answer("Только администратор может выбирать группу", show_alert=True)
        return

    group_number = int(cb.data.split(":", 1)[1])

    chat_id = cb.message.chat.id
    await subscribed_groups_dao.add_group(group_id=chat_id, subscribed_group_id=group_number)
    await cb.message.edit_text(
        f"✅ Для этого чата установлена пересылка расписания группы <b>{group_number}</b>",
        parse_mode='HTML'
    )
    await cb.answer("Группа установлена")


@group_router.callback_query(F.data == "grp_off")
async def set_group_off_callback(cb: CallbackQuery, subscribed_groups_dao: FromDishka[SubscribedGroupsDAO]) -> None:
    member = await cb.message.bot.get_chat_member(
        chat_id=cb.message.chat.id,
        user_id=cb.from_user.id
    )
    if member.status not in ("administrator", "creator"):
        await cb.answer("Только администратор может отключить пересылку", show_alert=True)
        return

    chat_id = cb.message.chat.id
    removed = await subscribed_groups_dao.remove_group(group_id=chat_id)
    if removed:
        await cb.message.edit_text("🔕 Пересылка расписания для этого чата отключена")
        await cb.answer("Отключено")
    else:
        await cb.answer("И так отключено")


@group_router.message(
    Command("start")
)
async def start_handler(message: Message) -> None:
    await message.reply("<u>Для личного использования</u> <a href='https://t.me/ngaek_official_bot?start'>перейдите</a> в <b>лс бота</b> и следуйте инструкции 🤖", parse_mode="HTML")
