from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, CallbackQuery
from datetime import date
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Calendar
from aiogram.filters import Command, CommandStart
from aiogram import Router, F
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from commands.keyboards.main_menu import create_inline_kb
from commands.keyboards.calendar_kb import create_calendar
from commands.lexicon.lexicon_ru import Lexicon_ru, now_month, now_year

# Инициализируем роутер уровня модуля
router: Router = Router()

# Создаем объект(ы) кнопок
button_start: KeyboardButton = KeyboardButton(text='start')

# Создаем объект(ы) клавиатуры для кнопок
keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[button_start]],
                                                    resize_keyboard=True,
                                                    )


# @router.message(CommandStart())
# async def start_command(message: Message):
#     await message.answer(text=Lexicon_ru['/start'],
#                          )


@router.message(CommandStart())
async def process_start_command(message: Message):
    keyboard_menu = create_inline_kb(1, 'calendar', 'new_event')
    await message.answer(
        text=Lexicon_ru['/start'],
        reply_markup=keyboard_menu
    )


@router.callback_query(F.data == 'calendar')
async def process_open_calendar(callback: CallbackQuery):
    await callback.message.edit_text(
        text='Календарь событий',
        reply_markup=create_calendar(3,
                                     'backward_c', f'{now_month}', 'forward_c',
                                     last_btn='Главное меню'))
    await callback.answer()


@router.callback_query(F.data == 'last_btn')
async def process_open_menu(callback: CallbackQuery):
    keyboard_menu = create_inline_kb(1, 'calendar', 'new_event')
    await callback.message.edit_text(
        text=Lexicon_ru['/start'],
        reply_markup=keyboard_menu
    )
    await callback.answer()


@router.callback_query(F.data == 'forward_c')
async def process_next_month(callback: CallbackQuery):
    global now_month
    if now_month < 12:
        now_month += 1
        await callback.message.edit_text(
            text='Календарь событий',
            reply_markup=create_calendar(3,
                                         'backward_c', f'{now_month}', 'forward_c',
                                         last_btn='Главное меню')
        )

    await callback.answer()
