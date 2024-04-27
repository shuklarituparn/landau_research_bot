import os
from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults

from bot.utils.translate_utils import translate, translate_english

load_dotenv()
"""Загружаем Ключи Доступа"""
TOKEN = os.getenv("GIGACHAT_API_AUTH")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY=")


async def ai_help(query):
    tavily_tool = TavilySearchResults(max_results=1)
    tools = [tavily_tool]
    search_query = translate_english.translate_text(query)
    response = tavily_tool.invoke({"query": search_query})
    # print(response)
    result = response[0]["content"]
    result_to_send = translate.translate_text(result)
    return result_to_send
