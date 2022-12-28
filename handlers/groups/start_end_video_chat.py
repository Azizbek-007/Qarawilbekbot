from aiogram import types 
from loader import dp
from filters import IsAdmin

@dp.message_handler(IsAdmin(), content_types=[types.ContentType.VIDEO_CHAT_SCHEDULED, types.ContentType.VOICE_CHAT_SCHEDULED ,types.ContentType.VIDEO_CHAT_STARTED, types.ContentType.VOICE_CHAT_STARTED, types.ContentType.VIDEO_CHAT_ENDED, types.ContentType.VOICE_CHAT_ENDED], chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP])
async def bot_group_chat(msg: types.Message):
    await msg.delete()