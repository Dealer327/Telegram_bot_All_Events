from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, CallbackQuery
from dateutil.relativedelta import relativedelta

from aiogram.filters import Command, CommandStart
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from ..services.file_handling import create_day, sorting_сalendar
from ....models import *
from ..keyboards.main_menu import create_inline_kb
from ..keyboards.calendar_kb import create_calendar, create_kb_yes_or_no, create_kb_finish_add_event
from ..lexicon.lexicon_ru import Lexicon_ru, Lexicon_month, Lexicon_form_new_event

# Инициализируем роутер уровня модуля
router: Router = Router()


class Form(StatesGroup):
    name_even = State()
    info_event = State()
    start_time = State()


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


@router.callback_query(F.data == 'new_event')
async def create_new_event(callback: CallbackQuery, state: FSMContext):
    keyboard_menu = create_inline_kb(1, last_btn='Главное меню')
    await state.set_state(Form.start_time)
    await callback.message.edit_text(
        text=f'{Lexicon_form_new_event["Date_event"]}',
        reply_markup=keyboard_menu
    )
    await callback.answer()


@router.message(Form.start_time)
async def process_input_date(message: Message, state: FSMContext):
    await state.update_data(start_time=message.text)
    try:
        date = datetime.strptime(message.text, '%d.%m.%Y')
        await message.answer(text=f"Вы ввели дату: {date.strftime('%d.%m.%Y')}")

    except ValueError:
        await message.answer(text='Еще раз')


@router.message(Form.name_even)
async def process_input_name_event(message: Message, state: FSMContext):
    await state.update_data(name_event=message.text)
    await message.answer(text=f"{Lexicon_form_new_event['Conf']}: {message.text}",
                         reply_markup=create_kb_yes_or_no(2, 'Yes', 'No')
                         )


@router.callback_query(F.data == 'Yes')
async def process_next_form(callback: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.set_state(Form.info_event)
    await callback.message.answer(text=f'{Lexicon_form_new_event["Info_event"]}')


@router.message(Form.info_event)
async def process_input_info_event(message: Message, state: FSMContext):
    await state.update_data(info_event=message.text)
    await message.answer(text=f'{Lexicon_form_new_event["Conf_info"]} {message.text}',
                         reply_markup=create_kb_finish_add_event(2, 'Reg', 'Cen')
                         )


@router.callback_query(F.data == 'Reg')
async def save_info_in_db(callback: CallbackQuery, state: FSMContext):
    p = await Profile.objects.aget(name=callback.from_user.username)
    data = await state.get_data()
    event = Event(name_event=data['name_event'],
                  info_event=data['info_event'],
                  user_create=p)
    await event.asave()
    await state.clear()
    # ДОДЕЛАТЬ: возможность добавлять одно событие
    keyboard_menu = create_inline_kb(1, 'calendar', 'new_event')

    await callback.message.answer(
        text=Lexicon_ru['/start'],
        reply_markup=keyboard_menu
    )


@router.callback_query(F.data == 'calendar')
async def process_open_calendar(callback: CallbackQuery):
    p = await Profile.objects.aget(external_id=callback.from_user.id)
    p.time_update: datetime = datetime.now()
    await p.asave(update_fields=['time_update'])
    p.choice_month = p.time_update
    await p.asave(update_fields=['choice_month'])
    name_month = callback.message.date.month
    list_months = create_day(callback.message.date.year)
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


@router.callback_query(lambda F: F.data == 'forward_c' or F.data == 'backward_c')
async def process_next_month(callback: CallbackQuery):
    m = await Profile.objects.aget(external_id=callback.from_user.id)
    if callback.data == 'forward_c':
        m.choice_month = m.choice_month + relativedelta(months=+1)
        await m.asave(update_fields=['choice_month'])
    else:
        m.choice_month = m.choice_month + relativedelta(months=-1)
        await m.asave(update_fields=['choice_month'])
    list_months = create_day(callback.message.date.year)
    days_in_month = sorting_сalendar(list_months, m.choice_month.month)
    await callback.message.edit_text(
        text=f'Календарь событий',
        reply_markup=create_calendar(3,
                                     days_in_month,
                                     'backward_c',
                                     f'{Lexicon_month[m.choice_month.month]}',
                                     'forward_c',
                                     last_btn='Главное меню')
    )
    await callback.answer()


@router.callback_query(lambda F: F.data == 'last_btn' or F.data == 'No' or F.data == 'Cen')
async def process_open_menu(callback: CallbackQuery):
    keyboard_menu = create_inline_kb(1, 'calendar', 'new_event')
    await callback.message.edit_text(
        text=Lexicon_ru['/start'],
        reply_markup=keyboard_menu
    )
    await callback.answer()
