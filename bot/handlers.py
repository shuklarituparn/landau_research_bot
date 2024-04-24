import os
import time

from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ContextTypes,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

import bot.utils.summarize.doc_summary
from bot.utils.speech2text import speech_to_text_audio, speech_to_text_voice
from bot.utils.text2speech import text_to_speech_impl
from bot import ai_helper

(
    SELECTING,
    SUMMARIZE_PAPER,
    AUDIO_SUMMARIZE,
    LISTEN_AND_SPEAK,
    TEXT_TO_SPEAK,
    CALL_AI,
) = range(6)

load_dotenv()  # loading the environment
SALUTE_SCOPE = os.getenv("SPEECH_SCOPE")
SALUTE_AUTH_DATA = os.getenv("SPEECH-AUTH-DATA")

keyboard = [["summarize", "listen"], ["Помог с защитой"]]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """
Добро пожаловать в бот для помочь по научной работе!! 
Пиши /help чтобы узнать больше!  
    """
    markUP = ReplyKeyboardMarkup(keyboard)
    await update.message.reply_text(text=text, reply_markup=markUP)
    return SELECTING


async def help_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="""
    Используйте следующие команды чтобы работать с ботом

1. /start   чтобы снова запустить бот
2. /help    Чтобы получить помочь
""",
    )


async def task_selector(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    # await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    # The program is not reaching here

    if text == "summarize":
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Отправь научную работу который хочешь суммизировать!",
        )
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="Предрочитано фото!"
        )
        return SUMMARIZE_PAPER
    elif text == "summarize_audio":
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="Спроси про что-то на научном"
        )
        return AUDIO_SUMMARIZE
    elif text == "listen":
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="Спроси про что-то на научном"
        )
        return LISTEN_AND_SPEAK
    elif text == "texting":
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Отправьте текст, чтобы получить аудио",
        )
        return TEXT_TO_SPEAK

    elif text == "Помог с защитой":
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Зову вашего помощника, подождите, пока он ответит на ваши вопросы! "
            "отправь end чтобы отменить",
        )
        return CALL_AI

    return SELECTING


async def summarize_paper(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file_id = update.message.document.file_id
    filename = update.message.document.file_name.strip()
    new_file = await context.bot.get_file(file_id)
    await new_file.download_to_drive(filename)
    text_to_send = await bot.utils.summarize.doc_summary.text_from_file(
        filename, update, context
    )
    # can actually gen a file id, and then send the user the file?
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_to_send)


async def summarize_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_audio = update.message.audio.file_id
    newfile = await context.bot.get_file(user_audio)
    filename = update.message.audio.file_name
    await newfile.download_to_drive(filename)
    Data = await speech_to_text_audio.speech_to_text_audio(
        filename,
        update=update,
        context=context,
        SALUTE_AUTH_DATA=SALUTE_AUTH_DATA,
        SALUTE_SCOPE=SALUTE_SCOPE,
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=Data)


async def listen_and_speak(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_voice = update.message.voice.file_id
    await context.bot.sendMessage(chat_id=update.effective_chat.id, text=user_voice)
    newfile = await context.bot.get_file(user_voice)
    await newfile.download_to_drive(user_voice)  # Here we send the user_ voice
    Data = await speech_to_text_voice.speech_to_text_voice(
        user_voice=user_voice,
        update=update,
        context=context,
        SALUTE_AUTH_DATA=SALUTE_AUTH_DATA,
        SALUTE_SCOPE=SALUTE_SCOPE,
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=Data)


async def text_to_speech(update: Update, context: ContextTypes.DEFAULT_TYPE):
    Data = await text_to_speech_impl.text_to_speech_impl(
        update=update,
        context=context,
        SALUTE_AUTH_DATA=SALUTE_AUTH_DATA,
        SALUTE_SCOPE=SALUTE_SCOPE,
    )
    await context.bot.send_audio(chat_id=update.effective_chat.id, audio=Data)


async def ask_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await ai_helper.ai_help(update, context)


async def end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Пока пока!")
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Был рад вам помочь!"
    )
    return ConversationHandler.END


conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        SELECTING: [
            MessageHandler(
                filters.Regex("^(summarize|listen|summarize_audio|texting)$"),
                task_selector,
            ),
        ],
        SUMMARIZE_PAPER: [
            MessageHandler(
                filters.Document and ~(filters.COMMAND | filters.Regex("^End|end$")),
                summarize_paper,
            ),
        ],
        AUDIO_SUMMARIZE: [
            MessageHandler(
                filters.AUDIO & ~(filters.COMMAND | filters.Regex("^End|end$")),
                summarize_audio,
            ),
        ],
        LISTEN_AND_SPEAK: [
            MessageHandler(
                filters.VOICE & ~(filters.COMMAND | filters.Regex("^End|end$")),
                listen_and_speak,
            ),
        ],
        TEXT_TO_SPEAK: [
            MessageHandler(
                filters.TEXT & ~(filters.COMMAND | filters.Regex("^End|end$")),
                text_to_speech,
            ),
        ],
        CALL_AI: [
            MessageHandler(
                filters.TEXT & ~(filters.COMMAND | filters.Regex("^End|end$")), ask_ai
            ),
        ],
    },
    fallbacks=[MessageHandler(filters.Regex("^End|end$"), end)],
    name="my_conv",
    persistent=True,
)

help_handler = CommandHandler("help", help_user)
