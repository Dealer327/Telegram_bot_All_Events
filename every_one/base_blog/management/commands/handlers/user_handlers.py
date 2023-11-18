from aiogram.types import Message, CallbackQuery
from dateutil.relativedelta import relativedelta

from aiogram.filters import CommandStart
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


from ..services.file_handling import create_day, create_button_main_menu
from ....models import *
from ..keyboards.main_menu import create_inline_kb
from ..keyboards.calendar_kb import create_calendar, create_kb_yes_or_no, create_kb_finish_add_event, create_list_events
from ..lexicon.lexicon_ru import Lexicon_ru, Lexicon_month, Lexicon_form_new_event
from ..date_base import datebase

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
        defaults={'name': message.from_user.username})
    await message.answer(
        text=Lexicon_ru['/start'],
        reply_markup=keyboard_menu
    )


@router.callback_query(F.data == 'new_event')
async def create_new_event(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Form.start_time)
    await callback.message.edit_text(
        text=f'{Lexicon_form_new_event["Date_event"]}',
        reply_markup=create_button_main_menu())
    await callback.answer()


@router.message(Form.start_time)
async def process_input_date(message: Message, state: FSMContext):
    await state.update_data(start_time=message.text)
    try:
        datetime.strptime(message.text, '%Y-%m-%d %H:%M').date()
        await state.set_state(Form.name_even)
        await message.answer(
            text=f"{Lexicon_form_new_event['Conf_date']} {message.text}",
            reply_markup=create_kb_yes_or_no(2, 'Yes_date', 'No_date')
        )
        await message.delete()
    except ValueError:
        await message.answer(text=f'{Lexicon_form_new_event["Error_date"]}')


@router.message(Form.name_even)
async def process_input_name_event(message: Message, state: FSMContext):
    await state.update_data(name_event=message.text)
    await state.set_state(Form.info_event)
    await message.answer(text=f"{Lexicon_form_new_event['Conf_name']} {message.text}",
                         reply_markup=create_kb_yes_or_no(2, 'Yes', 'No'))
    await message.delete()


@router.callback_query(lambda F: F.data == 'Yes' or F.data == 'Yes_date')
async def process_next_form(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'Yes':
        current_state = await state.get_state()
        if current_state is None:
            return
        await callback.message.edit_text(text=f'{Lexicon_form_new_event["Info_event"]}',
                                         reply_markup=create_button_main_menu())
        await callback.answer()
    else:
        await callback.message.edit_text(text=f'{Lexicon_form_new_event["Hi_event"]}',
                                         reply_markup=create_button_main_menu())
        await callback.answer()


@router.message(Form.info_event)
async def process_input_info_event(message: Message, state: FSMContext):
    await state.update_data(info_event=message.text)
    data = await state.get_data()
    await message.answer(text=f'{Lexicon_form_new_event["Conf_info"]} '
                              f'{data["name_event"]} '
                              f'{data["info_event"]} '
                              f' {data["start_time"]}',
                         reply_markup=create_kb_finish_add_event(2, 'Reg', 'Cen')
                         )
    await message.delete()


@router.callback_query(F.data == 'Reg')
async def save_info_in_db(callback: CallbackQuery, state: FSMContext):
    p = await Profile.objects.aget(name=callback.from_user.username)
    data = await state.get_data()
    event = Event(name_event=data['name_event'],
                  info_event=data['info_event'],
                  user_create=p,
                  start_time=data['start_time'])
    await event.asave()
    await state.clear()
    # ДОДЕЛАТЬ: возможность добавлять одно событие
    keyboard_menu = create_inline_kb(1, 'calendar', 'new_event')
    await callback.message.edit_text(
        text=Lexicon_ru['/start'],
        reply_markup=keyboard_menu
    )
    await callback.answer()


@router.callback_query(F.data == 'calendar')
async def process_open_calendar(callback: CallbackQuery):
    print(callback.message.from_user.id)
    p = await datebase.up_date_time_for_user(callback)
    name_month = callback.message.date.month
    list_days = create_day(callback.message.date.year, callback.message.date.month)
    events = await datebase.show_events_now_month(p.time_update.year, p.time_update.month)
    await callback.message.edit_text(
        text=f'<b>Календарь событий {p.choice_month.year}</b> ',
        reply_markup=create_calendar(3,
                                     events,
                                     list_days,
                                     'backward_c',
                                     f'{Lexicon_month[name_month]}',
                                     'forward_c',
                                     last_btn='Главное меню'))
    await callback.answer()


@router.callback_query(lambda c: c.data and c.data.isdigit() and int(c.data) <= 31)
async def process_pres_day(callback: CallbackQuery):
    events = await datebase.show_events_press_day(int(callback.data), callback.from_user.id)
    await callback.message.edit_text(text='Список',
                                     reply_markup=create_list_events(
                                         width=1,
                                         events=events,
                                         last_btn='Главное меню'
                                     ))
    await callback.answer()


@router.callback_query(lambda F: F.data == 'forward_c' or F.data == 'backward_c')
async def process_next_month(callback: CallbackQuery):
    m = await Profile.objects.aget(external_id=callback.from_user.id)
    if callback.data == 'forward_c':
        m.choice_month = m.choice_month + relativedelta(months=+1, day=1)
        await m.asave(update_fields=['choice_month'])
    else:
        m.choice_month = m.choice_month + relativedelta(months=-1, day=1)
        await m.asave(update_fields=['choice_month'])
    list_days = create_day(m.choice_month.year, m.choice_month.month)
    events = await datebase.show_events_now_month(m.choice_month.year, m.choice_month.month, )
    await callback.message.edit_text(
        text=f'<b>Календарь событий {m.choice_month.year}</b> ',
        reply_markup=create_calendar(3,
                                     events,
                                     list_days,
                                     'backward_c',
                                     f'{Lexicon_month[m.choice_month.month]}',
                                     'forward_c',
                                     last_btn='Главное меню')
    )
    await callback.answer()


@router.callback_query(lambda F: F.data == 'last_btn' or F.data == 'No' or F.data == 'Cen' or F.data == 'No_date')
async def process_open_menu(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    chat_id = callback.message.chat.id
    keyboard_menu = create_inline_kb(1, 'calendar', 'new_event')
    await callback.message.edit_text(
        text=Lexicon_ru['/start'],
        reply_markup=keyboard_menu)
    await callback.answer()
