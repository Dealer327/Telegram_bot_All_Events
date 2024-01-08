from datetime import datetime

from django.db.models import Q

from base_blog.models import *


async def create_new_user(user_info):
    await Profile.objects.aget_or_create(
        external_id=user_info.from_user.id,
        defaults={'name': user_info.from_user.username}
    )


async def take_user_from_db(user_name):
    p = await Profile.objects.aget(name=user_name)
    return p


# функция для обновления поля выбранный месяц в таблице профиль
async def up_date_time_for_user(callback):
    p = await Profile.objects.aget(external_id=callback.from_user.id)
    p.time_update: datetime = datetime.now()
    await p.asave(update_fields=['time_update'])
    p.choice_month = p.time_update
    await p.asave(update_fields=['choice_month'])
    return p


# функция для отображения счетчика не прочитанных эвентов в главном меню
async def show_count_not_read_event_in_menu(callback_id):
    p = await Profile.objects.aget(external_id=callback_id)
    events_in_menu = []
    events_not_read = []
    dt_all_events = datetime.now().strftime('%Y-%m-%d')
    # смотрим эвенты по дате начала и опубликованы ли они
    async for a in Event.objects.filter(Q(start_time__gte=dt_all_events) & Q(publish=True)):
        events_in_menu.append(a.id)
    # смотрим какие эвенты пользователь уже видел
    async for e in EventIsRead.objects.filter(profile=p).values_list('event', flat=True):
        events_not_read.append(e)

    count_not_read = 0
    # проверяем кол-во не просмотренных эвентов
    for i in events_in_menu:
        if i not in events_not_read:
            count_not_read += 1

    return count_not_read


# функция для отображения эвентов в меню календарь по выбранному месяцу
async def show_events_now_month(user, year, month, day):
    profile = await Profile.objects.aget(external_id=user)
    month_start = datetime(year, month, day)
    month_end = datetime(year=year,
                         month=month + 1,
                         day=1) if month < 12 else datetime(year=year + 1, month=1, day=1)
    all_events = []
    events_not_read = []
    events_read = []
    # фильтрации просмотренных эвентов
    async for u in EventIsRead.objects.filter(profile=profile).values_list('event', flat=True):
        events_read.append(u)
    # фильтрация эвентов по заданным временным рамкам и проверка просмотрено уже или нет
    async for e in Event.objects.filter(Q(start_time__gte=month_start) & Q(start_time__lt=month_end) & Q(publish=True)):
        if e.id in events_read:
            all_events.append(str(e.start_time.day))
        else:
            all_events.append(str(e.start_time.day))
            events_not_read.append(str(e.start_time.day))
    return all_events, events_not_read


# функция отображения списка эвентов на выбранное конкретное число в меню календаря
async def show_events_press_day(day, user):
    """ Фильтрация всех мероприятий и отборка просмотренных,
        для разного отображения у юзера эвентов которые он еще не смотрел"""
    profile = await Profile.objects.aget(external_id=user)
    start_date = datetime(profile.choice_month.year, profile.choice_month.month, day, 0, 0)
    end_date = datetime(profile.choice_month.year, profile.choice_month.month, day, 23, 59)
    events_day = []
    events_read = []
    events_not_read = []
    async for u in EventIsRead.objects.filter(profile=profile).values_list('event', flat=True):
        events_read.append(u)
    async for e in Event.objects.filter(start_time__range=(start_date, end_date)).order_by('start_time'):
        if e.id in events_read:
            events_day.append(e)
        else:
            events_day.append(e)
            events_not_read.append(e)
    return events_day, events_not_read


# функция выбора определенного эвента в списке эвентов заданной даты
async def show_info_about_event(id_event: int):
    e = await Event.objects.aget(id=id_event)
    return e


# функция добавления нового эвента в бот(для админов)
async def add_new_event(id_event: int):
    e = await Event.objects.aget(id=id_event)
    e.publish = True
    await e.asave(update_fields=['publish'])


# получения списка всех админов
async def all_admins():
    admins = []
    async for a in Admin.objects.all():
        admins.append(a.external_id)
    return admins


# получения списка всех юзеров
async def all_users():
    users = []
    async for u in Profile.objects.all():
        users.append(u)
    return users


# выборка эвента для постинга его в канал(Не в бот, а ботом в другой канал)
async def process_posting_event_in_chanel(id_event):
    event = await Event.objects.aget(id=id_event)
    return event


async def url_in_chanel_for_events(id_event: int, id_event_in_chanel: int):
    event = await Event.objects.aget(id=id_event)
    event.chanel = id_event_in_chanel
    await event.asave(update_fields=['chanel'])
