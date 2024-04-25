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

load_dotenv()
GIGACHAT_CREDENTIALS = os.getenv("GIGACHAT_API_AUTH")
RESEND_API_KEY = os.getenv("RESEND_API_KEY")


async def generate_find_the_paper(user_query):
    arxiv = ArxivAPIWrapper()
    docs = arxiv.run(user_query)
    return docs


# we use this to convert this to text
