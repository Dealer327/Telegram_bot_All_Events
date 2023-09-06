from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message, ContentType

from every_one.settings import TOKEN

API_TOKEN: str = TOKEN

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


@dp.message(Command(commands=['start']))
async def process_start_command(message: Message):
    await message.answer('Тест запущен', print(message.chat.username))






dp.run_polling(bot)
