from aiogram import types 
from loader import dp
from filters import IsAdmin

@dp.message_handler(IsAdmin(), content_types=[types.ContentType.ANY], chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP])
async def bot_ention(msg: types.Message):
    get_chat = await dp.bot.get_chat_member(msg.chat.id, msg.from_id)
    status_list = ['administrator', 'creator']
    if get_chat.status not in status_list:
        link_list = ['mention', 'url', 'text_link', 'text_mention']
        try:
            entity = msg.entities[0].type
            if entity in link_list:
                await msg.delete()
        except:
            try:
                entity_caption = msg.caption_entities[0].type
                if entity_caption in link_list:
                    await msg.delete()
            except: pass
    