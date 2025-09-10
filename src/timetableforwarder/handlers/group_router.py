from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums.chat_type import ChatType
from dishka.integrations.aiogram import FromDishka

from timetableforwarder.middlewares.is_admin_in_group_filter import IsAdminFilter 
from timetableforwarder.database.dao.subscribed_groups_dao import SubscribedGroupsDAO


group_router = Router()
group_router.message.filter(F.chat.type.in_({ChatType.GROUP, ChatType.SUPERGROUP}))


@group_router.message(
    Command("set_group"),
    IsAdminFilter()          
)
async def set_group_handler(message: Message, subscribed_groups_dao: FromDishka[SubscribedGroupsDAO]) -> None:
    args = message.text.split()
    
    if len(args) < 2:
        await message.reply("Укажите номер группы после команды. Пример: /set_group 2124")
        return
        
    group_arg = args[1]
    try:
        group_number = int(group_arg)
    except ValueError:
        await message.reply("Номер группы должен быть числом. Пример: /set_group 2124")
        return

    chat_id = message.chat.id
    await subscribed_groups_dao.add_group(group_id=chat_id, subscribed_group_id=group_number)
    await message.reply(f"✅ Отлично! Для этого чата установлена пересылка расписания группы {group_number}")


@group_router.message(
    Command("start")
)
async def start_handler(message: Message) -> None:
    await message.reply("<u>Для личного использования</u> <a href='https://t.me/ngaek_official_bot?start'>перейдите</a> в <b>лс бота</b> и следуйте инструкции 🤖", parse_mode="HTML")
