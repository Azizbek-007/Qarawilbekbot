from aiogram.dispatcher.filters.state import StatesGroup, State

class StateSendMessage(StatesGroup):
    promis = State()

class StateSendMessageGroup(StatesGroup):
    promis = State()
    msg = State()
