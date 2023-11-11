from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from ..lexicon.lexicon_ru import Lexicon_month, Lexicon_form_new_event


def create_kb_yes_or_no(width, *args):
    kb_yes_no = InlineKeyboardBuilder()
    buttons = []
    if args:
        for button in args:
            buttons.append(InlineKeyboardButton(
                text=Lexicon_form_new_event[button] if button in Lexicon_form_new_event else button,
                callback_data=button
            ))
    kb_yes_no.row(*buttons, width=width)
    return kb_yes_no.as_markup()


def create_kb_finish_add_event(width, *args):
    kb_yes_no = InlineKeyboardBuilder()
    buttons = []
    if args:
        for button in args:
            buttons.append(InlineKeyboardButton(
                text=Lexicon_form_new_event[button] if button in Lexicon_form_new_event else button,
                callback_data=button
            ))
    kb_yes_no.row(*buttons, width=width)
    return kb_yes_no.as_markup()


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
