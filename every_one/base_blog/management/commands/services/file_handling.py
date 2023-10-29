from calendar import monthrange


def create_day(year):
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


def sorting_сalendar(months: create_day, number_month: int):
    return months[number_month]
