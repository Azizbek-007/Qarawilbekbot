

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from loader import bot, bot_id
from utils.db_api import DBS

class IsAdmin(BoundFilter):

    async def check(self, message: types.Message):
        get_chat = await bot.get_chat_member(message.chat.id, bot_id)
        if get_chat.status == 'administrator': return True

class IsBadText(BoundFilter):
    async def check(self, message: types.Message):
       for x in message.text.split(" "):
            if x in DBS.bad_text_list(DBS):
                return True