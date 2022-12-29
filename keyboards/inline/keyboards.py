from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def start_btn(bot_username):
    return InlineKeyboardMarkup().add(
            InlineKeyboardButton(text="Есабат", callback_data="esabat")).add(
            InlineKeyboardButton(text="Ботты группаға қосыў", url=f"https://t.me/{bot_username}?startgroup=new")
            )

admin_btn = InlineKeyboardMarkup().add(
                InlineKeyboardButton(text="userslerge xabar jiberiw", callback_data="sendUsers")).add(
                InlineKeyboardButton(text="Grouppalarga xabar jiberiw", callback_data="sendGroup")
            ).add(
                InlineKeyboardButton(text="Bad Text", callback_data="bad_text"),
                InlineKeyboardButton(text="Grouppalar", callback_data="group_list")
            ).add(
                InlineKeyboardButton(text="Bazani jan'alaw", callback_data="update_baza")
            ).add(
                InlineKeyboardButton("Gruppaga xabar jiberiw", callback_data="send_message_group")
            )
def send_types(_type): 
    return InlineKeyboardMarkup().add(
                InlineKeyboardButton(text="Send Message", callback_data=f"SendMessage={_type}")).add(
                InlineKeyboardButton(text="Send Forward", callback_data=f"SendForward={_type}")).add(
                InlineKeyboardButton("cancel", callback_data='cancel'))

cencel_btn = InlineKeyboardMarkup().add(InlineKeyboardButton("cancel", callback_data='cancel'))

def pagination_btn(_min, _max):
    return InlineKeyboardMarkup().add(
            InlineKeyboardButton("◀️", callback_data=f"back={_min}={_max}"),
            InlineKeyboardButton("▶️", callback_data=f"next={_min}={_max}")).add(
            InlineKeyboardButton("cancel", callback_data='cancel'))
            

def share_btn(bot_username):
    return InlineKeyboardMarkup().add(
        InlineKeyboardButton("Группаға қосыў", url=f"https://t.me/{bot_username}?startgroup=new")
    )