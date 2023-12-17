import asyncio
import logging

from django.core.management import BaseCommand

from aiogram.fsm.storage.redis import RedisStorage, Redis
from aiogram import Bot, Dispatcher

from .config_data.config import Config, load_config
from .handlers import user_handlers, admin_hundlers

# Инициализация логгера
logger = logging.getLogger(__name__)
config: Config = load_config()

redis = Redis(host='localhost')
storage = RedisStorage(redis=redis)


class Command(BaseCommand):
    help = 'TT'

    async def handle(self, *args, **options):
        bot: Bot = Bot(token=self.tg_bot.token,
                       parse_mode='HTML')
        dp: Dispatcher = Dispatcher(storage=storage)

        dp.include_router(user_handlers.router)
        dp.include_router(admin_hundlers.router)

        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)


asyncio.run(Command.handle(config))
