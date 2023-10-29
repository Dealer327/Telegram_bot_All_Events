import asyncio
import logging

from django.core.management import BaseCommand


from aiogram import Bot, Dispatcher, types, F

from .config_data.config import Config, load_config
from .handlers import user_handlers

# Инициализация логгера
logger = logging.getLogger(__name__)
config: Config = load_config()


class Command(BaseCommand):
    help = 'TT'

    async def handle(self, *args, **options):
        bot: Bot = Bot(token=self.tg_bot.token,
                       parse_mode='HTML')
        dp: Dispatcher = Dispatcher()

        dp.include_router(user_handlers.router)

        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)


asyncio.run(Command.handle(config))
# Функция конфигурирования и запуск бота
# async def main() -> None:
#     # Конфигурация логирования
#     # logging.basicConfig(
#     #     level=logging.INFO,
#     #     format='%(filename)s:%((lineno)d #%(levelname)-8s'
#     #            '[%(asctime)s] - %(name)s - %(message)s'
#     # )
#     # logger.info('Starting bot')
#     #
#     config: Config = load_config()
#     # Инициализируем бота и диспетчер
#     bot: Bot = Bot(token=config.tg_bot.token,
#                    parse_mode='HTML')
#     dp: Dispatcher = Dispatcher()
#
#     # Настройка главного меню бота
#
#     await set_main_menu(bot)
#
#     # Регистрируем роутер(s) в диспетчере
#     dp.include_router(user_handlers.router)
#
#     # Пропускаем накопившиеся апдейты и запускаем polling
#     await bot.delete_webhook(drop_pending_updates=True)
#     await dp.start_polling(bot)
#
#
# if __name__ == '__main__':
#     asyncio.run(main())
