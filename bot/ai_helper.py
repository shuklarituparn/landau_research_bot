import os
from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ContextTypes
from langchain_community.retrievers import TavilySearchAPIRetriever

load_dotenv()
"""Загружаем Ключи Доступа"""
TOKEN = os.getenv("GIGACHAT_API_AUTH")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY=")


async def ai_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = GigaChat(credentials=TOKEN, verify_ssl_certs=False)
    #
    # messages = [
    #     SystemMessage(
    #         content=""
    #     )
    # ]

    retriever = TavilySearchAPIRetriever(k=3)

    result = retriever.invoke(update.message.text)  #getting the search result

    """Получение текста от пользователя и отправка ответа от помощника пользователю"""
    # user_input = update.message.text
    # messages.append(HumanMessage(content=user_input))
    # res = chat(messages)
    # messages.append(res)
    return result
