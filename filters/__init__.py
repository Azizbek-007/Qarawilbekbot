from aiogram import Dispatcher

from loader import dp
from .isAdmin import IsAdmin, IsBadText


if __name__ == "filters":
    dp.filters_factory.bind(IsAdmin)
    dp.filters_factory.bind(IsBadText)
    pass
