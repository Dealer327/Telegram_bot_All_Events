from django.db.models import Q

from ....models import *


async def up_date_time_for_user(callback):
    p = await Profile.objects.aget(external_id=callback.from_user.id)
    p.time_update: datetime = datetime.now()
    await p.asave(update_fields=['time_update'])
    p.choice_month = p.time_update
    await p.asave(update_fields=['choice_month'])
    return p


async def show_count_not_read_event_in_menu(cb):
    p = await Profile.objects.aget(external_id=cb)
    events_in_menu = []
    events_not_read = []
    dt_all_events = datetime.now().strftime('%Y-%m-%d')
    async for a in Event.objects.filter(Q(start_time__gte=dt_all_events) & Q(publish=True)):
        events_in_menu.append(a.id)

    async for e in EventIsRead.objects.filter(profile=p).values_list('event', flat=True):
        events_not_read.append(e)
    count_not_read = 0

    for i in events_in_menu:
        if i not in events_not_read:
            count_not_read += 1
    return count_not_read


async def show_count_not_read_events(user):
    events = []
    async for u in EventIsRead.objects.filter(profile=user).values_list('event', flat=True):
        events.append(u)
    return events


async def show_events_now_month(year, month, day):
    month_start = datetime(year, month, day)
    month_end = datetime(year=year,
                         month=month + 1,
                         day=1) if month < 12 else datetime(year=year + 1, month=1, day=1)
    events = []
    async for e in Event.objects.filter(Q(start_time__gte=month_start) & Q(start_time__lt=month_end) & Q(publish=True)):
        events.append(str(e.start_time.day))
    return events


async def show_events_press_day(day, cb):
    p = await Profile.objects.aget(external_id=cb)
    start_date = datetime(p.choice_month.year, p.choice_month.month, day, 0, 0)
    end_date = datetime(p.choice_month.year, p.choice_month.month, day, 23, 59)
    events_day = []
    async for e in Event.objects.filter(start_time__range=(start_date, end_date)).order_by('start_time'):
        events_day.append(e)
    return events_day


async def show_info_about_event(id_event: int):
    e = await Event.objects.aget(id=id_event)
    return e
