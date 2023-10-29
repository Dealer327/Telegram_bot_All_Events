from calendar import monthrange
from datetime import datetime

Lexicon_ru: dict[str, str] = {'/start': '<b>Привет, друг!</b>\n\nЭто бот,'
                                        'в котором ты сможешь узнать о предстоящих мероприятиях в твоем городе или'
                                        ' создать свои! Ты сможешь находить друзей и единомышленников в одном месте!',
                              'forward': '>>',
                              'backward': '<<',
                              'calendar': 'календарь событий',
                              'new_event': 'создать свое событие',
                              }


def create_now_days():
    days = monthrange(datetime.now().year, datetime.now().month)[1]
    lexicon_days: list[str] = [str(i) for i in range(1, days + 1)]
    return lexicon_days


def create_next_or_prior_month(year: int, month: int):
    days = monthrange(year, month)[1]
    lexicon_days: list[str] = [str(i) for i in range(1, days + 1)]
    return lexicon_days


def create_d(year):
    ready_days_in_month = [[]]
    list_days = []
    month = 1

    for i in range(12):
        days = monthrange(year, month)[1]
        for j in range(1, days + 1):
            list_days.append(str(j))
        ready_days_in_month.append(list_days)
        list_days = []
        month += 1
    return ready_days_in_month


def sorting_сalendar(months: create_d, number_month: int):
    return months[number_month]


month_now = 0

Lexicon_month: dict[str, str] = {1: 'Январь', 2: 'Февраль',
                                 3: 'Март', 4: 'Апрель',
                                 5: 'Май', 6: 'Июнь',
                                 7: 'Июль', 8: 'Август',
                                 9: 'Сентябрь', 10: ' Октябрь',
                                 11: 'Ноябрь', 12: 'Декабрь',
                                 'forward_c': '>>',
                                 'backward_c': '<<',
                                 }
LEXICON_COMMANDS: dict[str, str] = {
    'help': 'Справочник по работе бота'}
