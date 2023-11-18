from calendar import monthrange

from ..keyboards.main_menu import create_inline_kb
from ....models import *


def create_day(year: datetime.year, month: datetime.month):
    ready_days_in_month = []
    days = monthrange(year, month)[1]
    for i in range(1, days + 1):
        ready_days_in_month.append(str(i))
    return ready_days_in_month


def create_button_main_menu():
    keyboard_menu = create_inline_kb(1, last_btn='Главное меню')
    return keyboard_menu
