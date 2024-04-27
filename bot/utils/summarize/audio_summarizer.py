import os
import json
import requests
from telegram import Update
from telegram.ext import ContextTypes
from langchain_community.chat_models import GigaChat
from langchain.prompts import load_prompt
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import JSONLoader
from dotenv import load_dotenv

load_dotenv()
GIGACHAD_CREDENTIALS = os.getenv("GIGACHAT_API_AUTH")


async def text_from_file(filename):
    giga = GigaChat(
        credentials=GIGACHAD_CREDENTIALS,
        scope="GIGACHAT_API_PERS",
        verify_ssl_certs=False,
    )
    map_prompt = load_prompt("./bot/utils/map.yaml")
    combine_prompt = load_prompt("./bot/utils/combine.yaml")
    chain = load_summarize_chain(
        giga,
        chain_type="map_reduce",
        map_prompt=map_prompt,
        combine_prompt=combine_prompt,
    )
    filepath = filename
    print(filepath)
    loader = JSONLoader(
        filepath, jq_schema=".", json_lines=True, text_content=False, content_key="text"
    )
    document = loader.load()
    print(document)

    summary = chain.invoke(
        {
            "input_documents": document,
            "map_size": "одно предложение",
            "combine_size": "три предложения",
        }
    )
    summary_text = summary.get("output_text", "")
    summary = (
        "Cудя по тексту, краткое описание выглядит следующим образом:" + summary_text
    )
    return summary


#
# if __name__=="__main__":
#     async def get_text():
#         data=await text_from_file("response.json")
#         print(data)
