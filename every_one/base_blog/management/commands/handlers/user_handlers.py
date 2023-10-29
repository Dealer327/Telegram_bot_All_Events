from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, CallbackQuery
from datetime import date, datetime
import asyncio
from aiogram.filters import Command, CommandStart
from aiogram import Router, F
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from asgiref.sync import sync_to_async, async_to_sync

from ....models import *
from ..keyboards.main_menu import create_inline_kb
from ..keyboards.calendar_kb import create_calendar
from ..lexicon.lexicon_ru import Lexicon_ru, create_now_days, Lexicon_month, create_d, sorting_сalendar, month_now

# Инициализируем роутер уровня модуля
router: Router = Router()

# Создаем объект(ы) кнопок
button_start: KeyboardButton = KeyboardButton(text='start')

# Создаем объект(ы) клавиатуры для кнопок
keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[button_start]],
                                                    resize_keyboard=True,
                                                    )


@router.message(CommandStart())
async def process_start_command(message: Message):
    keyboard_menu = create_inline_kb(1, 'calendar', 'new_event')
    await Profile.objects.aget_or_create(
        external_id=message.from_user.id,
        defaults={
            'name': message.from_user.username
        }
    )
    await message.answer(
        text=Lexicon_ru['/start'],
        reply_markup=keyboard_menu
    )


@router.callback_query(F.data == 'calendar')
async def process_open_calendar(callback: CallbackQuery):
    p = await Profile.objects.aget(external_id=callback.from_user.id)
    p.time_update: datetime = datetime.now()
    await p.asave(update_fields=['time_update'])
    p.choice_month = p.time_update.month
    await p.asave(update_fields=['choice_month'])
    name_month = callback.message.date.month
    list_months = create_d(callback.message.date.year)
    days_in_month = sorting_сalendar(list_months, name_month)
    await callback.message.edit_text(
        text=f'Календарь событий',
        reply_markup=create_calendar(3,
                                     days_in_month,
                                     'backward_c',
                                     f'{Lexicon_month[name_month]}',
                                     'forward_c',
                                     last_btn='Главное меню')
    )
    await callback.answer()


@router.callback_query(F.data == 'forward_c')
async def process_next_month(callback: CallbackQuery):
    m = await Profile.objects.aget(external_id=callback.from_user.id)
    next_month = m.choice_month
    if next_month == 12:
        m.choice_month = 1
        await m.asave(update_fields=['choice_month'])
    elif next_month < 12:
        m.choice_month += 1
        await m.asave(update_fields=['choice_month'])
    list_months = create_d(callback.message.date.year)
    days_in_month = sorting_сalendar(list_months, m.choice_month)

    await callback.message.edit_text(
        text=f'Календарь событий',
        reply_markup=create_calendar(3,
                                     days_in_month,
                                     'backward_c',
                                     f'{Lexicon_month[m.choice_month]}',
                                     'forward_c',
                                     last_btn='Главное меню')
    )
    await callback.answer()


@router.callback_query(F.data == 'backward_c')
async def process_previous_month(callback: CallbackQuery):
    m = await Profile.objects.aget(external_id=callback.from_user.id)
    next_month = m.choice_month
    if next_month == 1:
        m.choice_month = 12
        await m.asave(update_fields=['choice_month'])
    elif next_month <= 12:
        m.choice_month -= 1
        await m.asave(update_fields=['choice_month'])
    list_months = create_d(callback.message.date.year)
    days_in_month = sorting_сalendar(list_months, m.choice_month)

    await callback.message.edit_text(
        text=f'Календарь событий',
        reply_markup=create_calendar(3,
                                     days_in_month,
                                     'backward_c',
                                     f'{Lexicon_month[m.choice_month]}',
                                     'forward_c',
                                     last_btn='Главное меню')
    )
    await callback.answer()


@router.callback_query(F.data == 'last_btn')
async def process_open_menu(callback: CallbackQuery):
    keyboard_menu = create_inline_kb(1, 'calendar', 'new_event')
    await callback.message.edit_text(
        text=Lexicon_ru['/start'],
        reply_markup=keyboard_menu
    )
    await callback.answer()
