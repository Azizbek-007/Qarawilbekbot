from aiogram import types
from loader import dp, bot_id
from filters import IsAdmin
from utils.db_api import DBS

@dp.message_handler(IsAdmin(), content_types=types.ContentTypes.NEW_CHAT_MEMBERS, chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP])
async def bot_new_chat_member(msg: types.Message):
    await msg.delete()

@dp.message_handler(content_types=types.ContentTypes.NEW_CHAT_MEMBERS, chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP])
async def bot_new_chat_member_(msg: types.Message):
    get_chat = await dp.bot.get_chat_member(msg.chat.id, bot_id)
    members_count = await msg.chat.get_members_count()
    DBS.register_group(DBS, msg.chat.invite_link, members_count, msg.chat.id, msg.chat.title, msg.from_id, get_chat.status)

@dp.message_handler(IsAdmin(), content_types=types.ContentTypes.LEFT_CHAT_MEMBER, chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP])
async def bot_left_chat_member(msg: types.Message):
    await msg.delete()
    