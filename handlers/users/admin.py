from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp, admin_list
from keyboards.inline import admin_btn, send_types, cencel_btn, pagination_btn
from states import StateSendMessage, StateSendMessageGroup
from utils.db_api import DBS
import asyncio

# @dp.message_handler(content_types='sticker')
# async def get_file_id(msg: types.Message):
#     print(msg)

@dp.message_handler(commands=['admin', 'panel'], chat_type=[types.ChatType.PRIVATE], user_id=admin_list)
async def hello_admin(msg: types.Message):
    await msg.answer("Hello Adimin", reply_markup=admin_btn)

@dp.message_handler(lambda msg: msg.text.startswith("/add=") or msg.text.startswith("/del="), chat_type=[types.ChatType.PRIVATE], user_id=admin_list)
async def bot_add_del_bad_text(msg: types.Message):
    text = msg.text.split('=')[1]
    if msg.text.startswith("/add="):
        DBS.add_bad_text(DBS, text)
        await msg.answer(f"<b>{text}</b> so'zi qosildi")
    else:
        DBS.del_bad_text(DBS, text)
        await msg.reply(f"<b>{text}</b> so'zi o'shirildi")

@dp.callback_query_handler(text="update_baza")
async def bot_update_baza(call: types.CallbackQuery):
    await call.answer("Loading...", True)
    await call.message.answer_sticker('CAACAgIAAxkBAAIU8mOskvpONtqSOQp2GPwFSwrx4yQtAAJLAgACVp29CmJQRdBQ-nGcLAQ')
    data = DBS.all_group_list(DBS)
    for x in data:
        try:
            await dp.bot.get_chat(x[3])
            DBS.set_group_status(DBS, 1, x[3])
        except: 
            DBS.set_group_status(DBS, 0, x[3])

    for y in DBS.user_list(DBS):
        try:
            await dp.bot.get_chat(y[0])
            DBS.set_user_status(DBS, 1, y[0])
        except: 
            DBS.set_user_status(DBS, 0, y[0])
    await call.message.answer("<b>Database successfuly Updated</b> 🥳")

@dp.callback_query_handler(text="send_message_group")
async def bot_send_message_to_group(call: types.CallbackQuery):
    await StateSendMessageGroup.promis.set()
    await call.message.delete()
    await call.message.answer("Gruppa idsin jiberin':", reply_markup=cencel_btn)

@dp.message_handler(regexp="^[-][0-9]+", state=StateSendMessageGroup.promis)
async def get_group_id(msg: types.Message, state: FSMContext):
    await state.finish()
    await state.update_data(chat_id=msg.text)
    await StateSendMessageGroup.msg.set()
    await msg.answer("Xabar jiberin'", reply_markup=cencel_btn)

@dp.message_handler(state=StateSendMessageGroup.promis)
async def dont_get_group_id(msg: types.Message, state: FSMContext):
    await msg.reply("Gruppa idisin qate kiritin'iz. Qayta kiritin'!")

@dp.message_handler(state=StateSendMessageGroup.msg, content_types=[types.ContentType.ANY])
async def send_msg_toGroup(msg: types.Message, state: FSMContext):
    try:
        get_data = await state.get_data()
        print(get_data['chat_id'])
        await msg.copy_to(get_data['chat_id'])
        await state.finish()
        await msg.reply("Xabar Jiberildi")
    except:  await msg.reply("Xabar jiberilmedi")
    
@dp.callback_query_handler(text="cancel")
async def bot_cancel(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()
    await call.message.answer("Hello Adimin", reply_markup=admin_btn)

@dp.callback_query_handler(text="bad_text")
async def bot_add_bad_text(call: types.CallbackQuery):
    await call.answer("So'z qosiw: \n/add=xyz\n\nSo'zdi o'shiriw\n/del=xyz", True)

@dp.callback_query_handler(text="sendUsers")
async def bot_send_message_users(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer("Xabar turin tan'lan':", reply_markup=send_types('User'))

@dp.callback_query_handler(text="sendGroup")
async def bot_send_message_groups(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer("Xabar turin tan'lan':", reply_markup=send_types("Group"))

@dp.callback_query_handler(lambda call: "SendMessage=" in call.data)
async def bot_send_message(call: types.CallbackQuery, state: FSMContext):
    data = str(call.data).split("=")
    await StateSendMessage.promis.set()
    await state.update_data(_type=data[0], msg=data[1])
    await call.message.delete()
    await call.message.answer("Xabar jiberin!", reply_markup=cencel_btn)

@dp.callback_query_handler(lambda call: "SendForward=" in call.data)
async def bot_send_forward(call: types.CallbackQuery, state: FSMContext):
    data = str(call.data).split("=")
    await StateSendMessage.promis.set()
    await state.update_data(_type=data[0], msg=data[1])
    await call.message.delete()
    await call.message.answer("Xabar jiberin!", reply_markup=cencel_btn)


@dp.callback_query_handler(text="group_list")
async def bot_group_list(call: types.CallbackQuery):
    text = ""
    data = DBS.group_list(DBS, 0, 30)
    for x in data:
        group_id = x[3]
        try:
            _count = await dp.bot.get_chat_member_count(group_id)
            group_data = await dp.bot.get_chat(group_id)
            text += f"<b>Group:</b> {group_data.title}\n<b>Group id:</b> {x[3]}\n<b>Group user:</b> {group_data.invite_link}\n<b>Group members:</b> {_count}\n\n"
        except: pass
    await call.message.answer(text, reply_markup=pagination_btn(0, 10), disable_web_page_preview=True)

@dp.callback_query_handler(lambda call: 'back=' in call.data)
async def back_pagination(call: types.CallbackQuery):
    data = call.data.split("=")
    _min = data[1]
    if int(_min) == 0:
        await call.answer("Maglumat tabilmadi")
    else:
        await call.message.delete()
        _max = int(data[2]) - 20
        data = DBS.group_list(DBS, int(_max), int(_min))
        text = ""
        for x in data:
            group_id = x[3]
            try:
                _count = await dp.bot.get_chat_member_count(group_id)
                group_data = await dp.bot.get_chat(group_id)
                text += f"<b>Group:</b> {group_data.title}\n<b>Group id:</b> {x[3]}\n<b>Group user:</b> {group_data.invite_link}\n<b>Group members:</b> {_count}\n\n"
            except: pass
        await call.message.answer(text, reply_markup=pagination_btn(0, 10), disable_web_page_preview=True)



@dp.callback_query_handler(lambda call: 'next=' in call.data)
async def next_pagination(call: types.CallbackQuery):
    data = call.data.split("=")
    _min, _max = data[2], int(data[2])+10
    data = DBS.group_list(DBS, int(_min), int(_max))
    if len(data) == 0: await call.answer("Maglumat tabilmadi")
    else:
        await call.message.delete()
        text = ""
        for x in data:
            group_id = x[3]
            try:
                _count = await dp.bot.get_chat_member_count(group_id)
                group_data = await dp.bot.get_chat(group_id)
                text += f"<b>Group:</b> {group_data.title}\n<b>Group id:</b> {x[3]}\n<b>Group user:</b> {group_data.invite_link}\n<b>Group members:</b> {_count}\n\n"
            except:pass
        await call.message.answer(text, reply_markup=pagination_btn(0, 10), disable_web_page_preview=True)

@dp.message_handler(state=StateSendMessage.promis, content_types=types.ContentTypes.ANY)
async def send_all_message_bot(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    await state.reset_state()
    s, n = 0, 0
    if data['_type'] == 'SendMessage':
        if data['msg'] == 'User':
            await msg.answer("Jiberilip atir...")
            for x in DBS._user_list(DBS):
                try:
                    await msg.copy_to(x[0])
                    s +=1
                    await asyncio.sleep(.07)
                except: n +=1
           
            await msg.answer(f"Jiberildi: {s}\nJiberilmedi: {n}")
        elif data['msg'] == 'Group':
            await msg.answer("Jiberilip atir...")
            for x in DBS._all_group_list(DBS):
                try:
                    await asyncio.sleep(.07)
                    await msg.copy_to(x[3], reply_markup=msg.reply_markup)
                    s +=1
                except: n +=1
            await msg.answer(f"Jiberildi: {s}\nJiberilmedi: {n}")

    elif data["_type"] == 'SendForward':
        if data['msg'] == 'User':
            await msg.answer("Jiberilip atir...")
            for x in DBS._user_list(DBS):
                try:
                    await asyncio.sleep(.07)
                    await msg.forward(chat_id=x[0])
                    s +=1
                except: n +=1
            await msg.answer(f"Jiberildi: {s}\nJiberilmedi: {n}")

        elif data['msg'] == 'Group':
            await msg.answer("Jiberilip atir...")
            for x in DBS._all_group_list(DBS):
                try:
                    await asyncio.sleep(.07)
                    await msg.forward(chat_id=x[3])
                    s +=1
                except: n +=1
            await msg.answer(f"Jiberildi: {s}\nJiberilmedi: {n}")
    
    await state.finish()
          

