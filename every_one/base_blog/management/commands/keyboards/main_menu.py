from aiogram import Bot
from aiogram.types import BotCommand, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from ..lexicon.lexicon_ru import LEXICON_COMMANDS, Lexicon_ru


async def set_main_menu(bot: Bot):
    main_menu_commands = [BotCommand(
        command=command,
        description=description
    ) for command, description in LEXICON_COMMANDS.items()]
    await bot.set_my_commands(main_menu_commands)


def create_inline_kb(width: int, events: int | None = None, *args: str,
                     last_btn: str | None = None) -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []

    # Заполняем список кнопками из аргументов args и kwargs
    if args:
        for button in args:
            if button == 'calendar':
                if events == 0 or events is None:
                    buttons.append(InlineKeyboardButton(
                        text=f'{Lexicon_ru[button]}' if button in Lexicon_ru else button,
                        callback_data=button))
                else:
                    buttons.append(InlineKeyboardButton(
                        text=f'{Lexicon_ru[button]} {str(events)}🔥' if button in Lexicon_ru else button,
                        callback_data=button))
            else:
                buttons.append(InlineKeyboardButton(
                    text=f'{Lexicon_ru[button]}' if button in Lexicon_ru else button,
                    callback_data=button))
    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=width)
    if last_btn:
        kb_builder.row(InlineKeyboardButton(
            text=last_btn,
            callback_data='last_btn'
        ))

    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()


def create_button_back_and_mani_menu(width: int, *args):
    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []

    if args:
        for button in args:
            buttons.append(InlineKeyboardButton(
                text=f'{Lexicon_ru[button]}' if button in Lexicon_ru else button,
                callback_data=button))
    kb_builder.row(*buttons, width=width)
    return kb_builder.as_markup()
