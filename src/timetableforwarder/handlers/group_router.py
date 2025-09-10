from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums.chat_type import ChatType
from timetableforwarder.middlewares.is_admin_in_group_filter import IsAdminFilter 


group_router = Router()
group_router.message.filter(F.chat.type.in_({ChatType.GROUP, ChatType.SUPERGROUP}))

@group_router.message(
    Command("set_group"),
    IsAdminFilter()          
)
async def set_group_handler(message: Message) -> None:
    args = message.text.split()
    
    if len(args) < 2:
        await message.reply("Пожалуйста, укажите номер группы после команды. Пример: /set_group 2145")
        return
        
    group_number = args[1]
    
    await message.reply(f"✅ Отлично! Для этого чата установлен номер группы: {group_number}")

@group_router.message(
    Command("start")
)
async def start_handler(message: Message) -> None:
    await message.reply("<u>Для личного использования</u> <a href='https://t.me/ngaek_official_bot?start'>перейдите</a> в <b>лс бота</b> и следуйте инструкции 🤖", parse_mode="HTML")
