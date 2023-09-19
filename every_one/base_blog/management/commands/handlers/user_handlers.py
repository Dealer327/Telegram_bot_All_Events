from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.filters import Command, CommandStart
from aiogram import Router
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from commands.lexicon.lexicon_ru import Lexicon_ru

# Инициализируем роутер уровня модуля
router: Router = Router()

# Создаем объект(ы) кнопок
button_start: KeyboardButton = KeyboardButton(text='start')

# Создаем объект(ы) клавиатуры для кнопок
keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[button_start]],
                                                    resize_keyboard=True,
                                                    )


@router.message(CommandStart())
async def start_command(message: Message):
    await message.answer(text=Lexicon_ru['/start'],
                         )
