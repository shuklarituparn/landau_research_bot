# listing the tools needed - GIGACHAT (LLM MODEL)
# Github for later, NASA, Wolfram Alpha
import os

from dotenv import load_dotenv
from langchain import hub
from langchain.agents import (
    AgentExecutor,
    create_openai_functions_agent,
    load_tools,
)
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent, load_tools
from langchain_community.chat_models import GigaChat
from langchain_community.utilities import ArxivAPIWrapper
from bot.utils.translate_utils import translate


async def generate_find_the_paper(user_query):
    arxiv = ArxivAPIWrapper()
    docs = arxiv.run(user_query)
    translated_text = await translate.translate_text(docs)
    return translated_text
