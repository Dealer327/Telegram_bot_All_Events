import asyncio

from aiogram import Bot, Dispatcher, types, F
from config_data.config import Config, load_config


# Функция конфигурирования и запуск бота
async def main() -> None:
    config: Config = load_config()

    bot: Bot = Bot(token=config.tg_bot.token)
    dp: Dispatcher = Dispatcher()

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())



