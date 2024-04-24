import os

from telegram.ext import ApplicationBuilder, PicklePersistence
from dotenv import load_dotenv

load_dotenv()  # loading the environment
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Получим токен доступа


def initialize_the_bot():
    """
    Функция, которая использует ключ доступа и возвращает бота для дальнейшего использования
    :return: Бот
    """
    my_persistence = PicklePersistence(filepath="./TelegramBot")
    application = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .persistence(persistence=my_persistence)
        .build()
    )
    return application
