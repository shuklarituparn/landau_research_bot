import os

from langchain_community.chat_models import GigaChat
from langchain_community.document_transformers import DoctranTextTranslator
from langchain_core.documents import Document
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()
GIGACHAT_CREDENTIALS = os.getenv("GIGACHAT_API_AUTH")


async def translate_text(content):
    chat = GigaChat(credentials=GIGACHAT_CREDENTIALS, verify_ssl_certs=False)

    messages = [
        SystemMessage(
            content="Вы действительно хороший переводчик, переведите следующий текст на английском языке"
        ),
        HumanMessage(content=content),
    ]

    res = chat(messages)
    messages.append(res)
    return res.content
