from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from ..lexicon.lexicon_ru import Lexicon_month, Lexicon_form_new_event, Lexicon_ru


# Класс для создания callback-данных для инлайн-клавиатур
class CallbackFactoryForEvent(CallbackData, prefix="Event", sep="_"):
    id_event: int


# Функция для создания инлайн-клавиатуры с кнопками "Да" или "Нет"
def create_kb_yes_or_no(width: int, *args: str) -> InlineKeyboardMarkup:
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


# Функция для создания инлайн-клавиатуры для завершения добавления события
def create_kb_finish_add_event(width: int, *args: str):
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


# Функция для создания инлайн-клавиатуры для календаря
def create_calendar(width: int,
                    events: tuple[list],
                    list_days: list[str],
                    *args,
                    last_btn: str | None = None) -> InlineKeyboardMarkup:
    kb_calendar = InlineKeyboardBuilder()
    buttons = []
    buttons_days = []
    all_events = events[0]
    events_not_read = events[1]
    if args:
        for button in args:
            buttons.append(InlineKeyboardButton(
                text=Lexicon_month[button] if button in Lexicon_month else button,
                callback_data=button
            ))

    for button_d in list_days:
        if button_d in all_events and button_d in events_not_read:

            buttons_days.append(InlineKeyboardButton(
                text=f'{button_d}({all_events.count(button_d)}) 🔥',
                callback_data=button_d
            ))
        elif button_d in all_events and button_d not in events_not_read:

            buttons_days.append(InlineKeyboardButton(
                text=f'{button_d}({all_events.count(button_d)})',
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


# Функция для создания инлайн-клавиатуры для списка событий
def create_list_events(width: int,
                       events: tuple[list],
                       *args) -> InlineKeyboardMarkup:
    kb_event_day = InlineKeyboardBuilder()
    buttons = []
    all_events = events[0]
    events_not_read = events[1]
    if args:
        for button in args:
            buttons.append(InlineKeyboardButton(
                text=f'{Lexicon_ru[button]}' if button in Lexicon_ru else button,
                callback_data=button
            ))
    for button in all_events:
        if button in events_not_read:
            buttons.append(InlineKeyboardButton(
                text=f'{button.start_time.strftime("%H:%M")} - {button.name_event}🔥',
                callback_data=CallbackFactoryForEvent(id_event=button.id
                                                      ).pack()
            ))
        else:
            buttons.append(InlineKeyboardButton(
                text=f'{button.start_time.strftime("%H:%M")} - {button.name_event} ✌',
                callback_data=CallbackFactoryForEvent(id_event=button.id
                                                      ).pack()
            ))
    kb_event_day.row(*buttons[::-1], width=width)
    return kb_event_day.as_markup()
