from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from loader import dp
from utils.db_api import DBS
from keyboards.inline import start_btn
from datetime import datetime
import pytz


@dp.message_handler(CommandStart())
@dp.throttled(rate=1)
async def bot_start(msg: types.Message):
    DBS.register_user(DBS, user=msg.from_id, username=msg.from_user.username,
        first_name=msg.from_user.first_name, last_name=msg.from_user.last_name)
    me = await dp.bot.get_me()
    await msg.answer(f'''
Ассалаўма әлейкум {msg.from_user.first_name} !

👨🏻‍✈ Мен группаңызды өзбекше, арабша рекламалар ҳәм басқада силтемелерден қорықлайман, кирди-шықты хабарларын өширип тураман!

❗️Буларды ислеўим ушын сизден талап етилетуғын нәрсе мени группаңызға қосып, админ қылыў! 😄

📃 Бот жаңалықлары: @''', reply_markup=start_btn(me.username))

@dp.callback_query_handler(text='esabat')
async def esabat(call: types.CallbackQuery):
    user_count = DBS.user_count(DBS)
    group_count = DBS.group_count(DBS)
    date = datetime.now(pytz.timezone('Asia/Tashkent')).strftime("%Y-%m-%d")
    _time = datetime.now(pytz.timezone('Asia/Tashkent')).strftime("%H:%M:%S")
    await call.answer(f'''
📊 Есабат 📈

👤 Пайдаланыўшылар: {user_count}
👥 Группалар: {group_count}
🔄 Жаңаланыўлар саны: 1

⏰{_time} 📆{date}''', True)

@dp.my_chat_member_handler()
async def ok(msg: types.Message):
    data = msg.new_chat_member
    if data.status == 'administrator':
        link = await dp.bot.export_chat_invite_link(msg.chat.id)
        members_count = await msg.chat.get_members_count()
        print(members_count)
        DBS.update_group(DBS, link, members_count, data.status, msg.chat.id)
        if data.can_delete_messages == True:
            await dp.bot.send_message(chat_id=msg.chat.id, text='Бот группаға админ қылынды! ✅')