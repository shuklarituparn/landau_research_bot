import os
from telegram import Update
from telegram.ext import ContextTypes

from langchain_community.chat_models import GigaChat
from langchain.prompts import load_prompt
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import PyPDFLoader  # importing the pdf loader
from dotenv import load_dotenv

load_dotenv()
GIGACHAD_CREDENTIALS = os.getenv("GIGACHAT_API_AUTH")


async def text_from_file(filename, update: Update, context: ContextTypes.DEFAULT_TYPE):
    giga = GigaChat(
        credentials=GIGACHAD_CREDENTIALS,
        scope="GIGACHAT_API_CORP",
        verify_ssl_certs=False,
    )
    # print(os.getcwd()) to text, it's located in the root
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
    loader = PyPDFLoader(filepath)  # loading the pdf
    documents = loader.load_and_split()
    # summary = chain.invoke({"input_documents": documents})   for the case when just want a summary
    summary = chain.invoke(
        {
            "input_documents": documents,
            "map_size": "одно предложение",
            "combine_size": "три предложения",
        }
    )

    summary_text = summary.get("output_text", "")

    summary = (
        "Cудя по тексту, краткое описание выглядит следующим образом:" + summary_text
    )
    return summary  # Summary of our text, need to see the multi-agent


# Can here convert it to the text to the speech and response


# TODO: Can use chroma to store all these in the collection and it will increase the memory
# TODO: Can store the data to the cloud and get the response id, store it and then let user decide when to download


# TODO: Need to make the helper function that checks the message type and sends uses the voice to audio converter
# TODO: streaming=True for big models where text gen requires more time
