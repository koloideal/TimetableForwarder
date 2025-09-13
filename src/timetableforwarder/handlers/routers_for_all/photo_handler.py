from io import BytesIO
from pprint import pprint
from aiogram.types import Message
from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest

from timetableforwarder.services.image_to_text import ImageToTextService
from timetableforwarder.utils.get_config import Config
from timetableforwarder.database.dao.users_dao import UsersDAO
from timetableforwarder.database.dao.subscribed_groups_dao import SubscribedGroupsDAO


def build_group_message(group: str, lessons: list[dict], date: str) -> str:
    header = (
        f"<b>📅 Расписание на <u>{date}</u></b>\n"
        f"<b>Группа: <u>{group}</u></b>\n\n"
    )
    if not lessons:
        return header + "<blockquote><i>Нет занятий</i></blockquote>"
    lines = []
    for item in sorted(lessons, key=lambda x: x.get("position", 0)):
        name = item.get("name", "—")
        pos = item.get("position", 0)
        audience = item.get("audience")
        if audience and audience != "not found":
            lines.append(f"{pos}. <b>{name}</b> (ауд. {audience})\n")
        else:
            lines.append(f"{pos}. <b>{name}</b>\n")
    return header + f"<blockquote>{'\n'.join(lines)}</blockquote>\n"


async def handle_channel_photo(
    message: Message,
    config: Config,
    users_dao: UsersDAO,
    subscribed_groups_dao: SubscribedGroupsDAO,
) -> None:
    if message.caption:
        return

    file_id = message.photo[-1].file_id
    buffer = BytesIO()
    await message.bot.download(
        file=file_id,
        destination=buffer
    )
    buffer.seek(0)
    image_bytes = buffer.read()

    image_to_text_service = ImageToTextService(api_key=config.plpx_key)

    await message.bot.send_message(config.creator_id, "Начало распознования текста расписания с изображения...")
    response = await image_to_text_service.converting_image_to_text(image_bytes)
    pprint(response)
    await message.bot.send_message(config.creator_id, "Текст расписания успешно распознано")

    if response.get("error") == "NOT_TIMETABLE":
        return None

    date_str: str = response.get("date", "—")
    timetable = response.get("timetable", [])
    group_to_text: dict[str, str] = {
        entry["group"]: build_group_message(entry["group"], entry.get("lessons", []), date_str)
        for entry in timetable
    }

    users = await users_dao.get_all_users()

    for user in users:
        subs_str = user.subscribed_groups
        if not subs_str:
            continue
        groups = [g for g in subs_str.split(":") if g]
        texts = [group_to_text[g] for g in groups if g in group_to_text]
        if not texts:
            continue
        if len(texts) == 1:
            line_separate = '\n'
        else:
            line_separate = '\n\n'
        final_text = "\n\n".join(texts) + f"{line_separate}<b><i>made by kolo</i></b>"
        try:
            await message.bot.send_message(
                chat_id=user.user_id, text=final_text, parse_mode="HTML"
            )
        except (TelegramForbiddenError, TelegramBadRequest):
            continue

    subscribed_groups = await subscribed_groups_dao.get_all_groups()

    for rec in subscribed_groups:
        target_group = str(rec.subscribed_group)
        chat_id = rec.group_id
        if not target_group:
            continue
        text = group_to_text.get(target_group)
        if not text:
            continue
        text += "\n<b><i>made by kolo</i></b>"
        try:
            sent = await message.bot.send_message(
                chat_id=chat_id, text=text, parse_mode="HTML"
            )
            await message.bot.pin_chat_message(
                chat_id=chat_id, message_id=sent.message_id, disable_notification=True
            )
        except (TelegramForbiddenError, TelegramBadRequest):
            continue
