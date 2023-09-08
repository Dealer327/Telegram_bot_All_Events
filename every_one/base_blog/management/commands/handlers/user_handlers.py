from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from ..lexicon.lexicon_ru import Lexicon_ru


@dp.message(CommandStart())
async def start_command(message: Message):
    await message.answer(text=Lexicon_ru['/start'])
