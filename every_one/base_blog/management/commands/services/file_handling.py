from calendar import monthrange
from datetime import datetime

from base_blog.management.commands.keyboards.main_menu import create_inline_kb


def create_day(year: datetime.year, month: datetime.month):
    ready_days_in_month = []
    days = monthrange(year, month)[1]
    for i in range(1, days + 1):
        ready_days_in_month.append(str(i))
    return ready_days_in_month


