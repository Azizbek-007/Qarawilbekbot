from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp
from keyboards.inline import admin_btn, send_types, cencel_btn
from states import StateSendMessage
from utils.db_api import DBS
import asyncio
@dp.message_handler(commands=['admin', 'panel'])
async def hello_admin(msg: types.Message):
    await msg.answer("Hello Adimin", reply_markup=admin_btn)

@dp.callback_query_handler(text="cancel")
async def bot_cancel(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()
    await call.message.answer("Hello Adimin", reply_markup=admin_btn)

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



@dp.message_handler(state=StateSendMessage.promis, content_types=types.ContentTypes.ANY)
async def send_all_message_bot(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    await state.reset_state()
    s, n = 0, 0
    if data['_type'] == 'SendMessage':
        if data['msg'] == 'User':
            try:
                for x in DBS.user_list(DBS):
                    await asyncio.sleep(.07)
                    await msg.copy_to(x[0], msg.reply_markup)
                    s +=1
                await msg.answer("Jiberilip atir...")
            except:
                n +=1
            await msg.answer(f"Jiberildi: {s}\nJiberilmedi{n}")
        elif data['msg'] == 'Group':

            try:
                for x in DBS.group_list(DBS):
                    await asyncio.sleep(.07)
                    await msg.copy_to(x[3], msg.reply_markup)
                    s +=1
                await msg.answer("Jiberilip atir...")
            except:
                n +=1
            await msg.answer(f"Jiberildi: {s}\nJiberilmedi{n}")

    elif data["_type"] == 'SendForward':
        if data['msg'] == 'User':
            try:
                for x in DBS.user_list(DBS):
                    await asyncio.sleep(.07)
                    await msg.forward(chat_id=x[3])
                    s +=1
                await msg.answer("Jiberilip atir...")
            except:
                pass
            await msg.answer(f"Jiberildi: {s}\nJiberilmedi{n}")
        elif data['msg'] == 'Group':
            try:
                for x in DBS.group_list(DBS):
                    await asyncio.sleep(.07)
                    await msg.forward(chat_id=x[3])
                    s +=1
                await msg.answer("Jiberilip atir...")
            except:
                n +=1
            await msg.answer(f"Jiberildi: {s}\nJiberilmedi{n}")
    
    await state.finish()
          

