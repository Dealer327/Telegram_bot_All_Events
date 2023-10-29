from calendar import monthrange
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime import datetime

from ..lexicon.lexicon_ru import Lexicon_ru, Lexicon_month, create_now_days


# def create_days(month: int, year: int):
#     days = monthrange(year, month)[1]
#     lexicon_days: list[str] = [str(i) for i in range(1, days + 1)]
#     return lexicon_days


def create_calendar(width, list_days, *args, last_btn: str | None = None):
    kb_calendar = InlineKeyboardBuilder()

    buttons = []
    buttons_days = []
    if args:
        for button in args:
            buttons.append(InlineKeyboardButton(
                text=Lexicon_month[button] if button in Lexicon_month else button,
                callback_data=button
            ))
    for button_d in list_days:
        buttons_days.append(InlineKeyboardButton(
            text=button_d if button_d in list_days else button_d,
            callback_data=button_d
        ))
    kb_calendar.row(*buttons, width=width).add(*buttons_days).adjust(3, 4)
    if last_btn:
        kb_calendar.row(InlineKeyboardButton(
            text=last_btn,
            callback_data='last_btn'
        ))
    return kb_calendar.as_markup()
