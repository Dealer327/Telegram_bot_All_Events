from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str  # Токен телеграм бота


@dataclass
class Config:
    tg_bot: TgBot


def load_config(path: str | None = None) -> Config:
    """Функция для создания экземпляра класса Config с параметрами локального файла .env,
    для защиты данных"""
    env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(token=env('TOKEN_BOT')))
