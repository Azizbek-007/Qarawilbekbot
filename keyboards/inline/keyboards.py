from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def start_btn(bot_username):
    return InlineKeyboardMarkup().add(
            InlineKeyboardButton(text="Есабат", callback_data="esabat")).add(
            InlineKeyboardButton(text="Ботты группаға қосыў", url=f"https://t.me/{bot_username}?startgroup=new")
            )