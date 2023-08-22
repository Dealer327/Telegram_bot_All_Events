import telebot
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Старт Телеграм бота'

    def handle(self, *args, **options):
        bot = telebot.TeleBot(settings.TOKEN, threaded=False)
        print(bot.get_me())
