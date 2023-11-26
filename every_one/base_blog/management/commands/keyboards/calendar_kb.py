from datetime import datetime

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from ..lexicon.lexicon_ru import Lexicon_month, Lexicon_form_new_event


class CallbackFactoryForEvent(CallbackData, prefix="Event", sep="_"):
    id_event: int


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


def create_calendar(width, events, list_days, *args, last_btn: str | None = None):
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
        if button_d in events:
            buttons_days.append(InlineKeyboardButton(
                text=f'{button_d}({events.count(button_d)})',
                callback_data=button_d
            ))
        else:
            buttons_days.append(InlineKeyboardButton(
                text=f'{button_d}',
                callback_data=button_d
            ))
    kb_calendar.row(*buttons, width=width).add(*buttons_days).adjust(3, 4)
    if last_btn:
        kb_calendar.row(InlineKeyboardButton(
            text=last_btn,
            callback_data='last_btn'
        ))
    return kb_calendar.as_markup()


def create_list_events(width, events, last_btn):
    kb_event_day = InlineKeyboardBuilder()
    buttons = []
    for button in events:
        buttons.append(InlineKeyboardButton(
            text=f'{button.start_time.strftime("%H:%M")} - {button.name_event}',
            callback_data=CallbackFactoryForEvent(id_event=button.id
                                                  ).pack()
        ))
    kb_event_day.row(*buttons, width=width)
    if last_btn:
        kb_event_day.row(InlineKeyboardButton(
            text=last_btn,
            callback_data='last_btn'
        ))
    return kb_event_day.as_markup()
