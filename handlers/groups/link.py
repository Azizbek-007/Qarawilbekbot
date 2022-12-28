from aiogram import types 
from loader import dp
from filters import IsAdmin
from keyboards.inline import share_btn
from aiogram.utils.exceptions import Throttled
from utils.db_api import DBS

@dp.message_handler(lambda msg: msg.text in DBS.bad_text_list(DBS), content_types=['text'])
async def bot_delete_bad_text(msg: types.Message):
    await msg.delete()
    get_me = await dp.bot.get_me()
    try:
        await dp.throttle(key='*', rate=10)
        await msg.answer(f"<a href='tg://user?id={msg.from_id}'>{msg.from_user.full_name}</a> <b>сөгинбең!</b>", reply_markup=share_btn(get_me.username))
    except Throttled: pass

@dp.message_handler(IsAdmin(), content_types=[types.ContentType.ANY], chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP])
async def bot_ention(msg: types.Message):
    get_chat = await dp.bot.get_chat_member(msg.chat.id, msg.from_id)
    get_me = await dp.bot.get_me()
    status_list = ['administrator', 'creator']
    if get_chat.status not in status_list:
        link_list = ['mention', 'url', 'text_link', 'text_mention']
        for x in msg.entities:
            if x.type in link_list:
                await msg.delete()
                try:
                    await dp.throttle(key='*', rate=10)
                    await msg.answer(f"<a href='tg://user?id={msg.from_id}'>{msg.from_user.full_name}</a> <b>реклама тарқатпаң!</b>", reply_markup=share_btn(get_me.username))
                except Throttled: pass
        else:
            for x in msg.caption_entities:
                if x.type in link_list:
                    await msg.delete()
                    try:
                        await dp.throttle(key='*', rate=10)
                        await msg.answer(f"<a href='tg://user?id={msg.from_id}'>{msg.from_user.full_name}</a> реклама тарқатпаң!", reply_markup=share_btn(get_me.username))
                    except Throttled: pass
                    
        
