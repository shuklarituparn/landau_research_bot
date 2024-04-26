import os

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
from bot import ai_helper
from bot.utils.multi_chain_brainstorm import brainstorm
from bot.utils.speech2text import speech_to_text_voice
from bot.utils.text2speech import text_to_speech_impl

(
    SELECTING,
    SUMMARIZE_PAPER,
    BRAINSTORM,
    ASSISTANT,
) = range(4)

load_dotenv()  # loading the environment
SALUTE_SCOPE = os.getenv("SPEECH_SCOPE")
SALUTE_AUTH_DATA = os.getenv("SPEECH-AUTH-DATA")

keyboard = [["summarize", "brainstorm"], ["assistant", "analyze"]]


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
3. summarize: Отправь научную работу который хочешь суммизировать! Также получи аудио суммари
4. brainstorm: Давайте поищем какие-нибудь научные работы!
""",
    )


async def task_selector(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    if text == "summarize":
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Отправь научную работу который хочешь суммизировать!",
        )
        return SUMMARIZE_PAPER
    elif text == "brainstorm":
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Давайте поищем какие-нибудь научные работы!",
        )
        return BRAINSTORM
    elif text == "assistant":
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="Спроси про что-то на научном"
        )
        return ASSISTANT

    return SELECTING


async def summarize_paper(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file_id = update.message.document.file_id
    filename = update.message.document.file_name.strip()
    new_file = await context.bot.get_file(file_id)
    await new_file.download_to_drive(filename)
    text_to_send = await bot.utils.summarize.doc_summary.text_from_file(
        filename, update, context
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Вот ваши суммари: "
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_to_send)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Подождите 30 секудн чтобы получить аудио суммари ",
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Вот ваши аудио-суммари: "
    )
    summary_file = open(f"{filename}.txt", "w+")
    summary_file.write(text_to_send)
    summary_file.close()
    await text_to_speech(f"{filename}.txt", update=update, context=context)


async def brainstorm_a_paper(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # test the brainstorm
    user_query = update.message.text
    print(user_query)
    text = await brainstorm.generate_find_the_paper(user_query=user_query)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)


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


async def text_to_speech(Filename, update: Update, context: ContextTypes.DEFAULT_TYPE):
    Data = await text_to_speech_impl.text_to_speech_impl(
        filename=Filename,
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
                filters.Regex("^(summarize|brainstorm|texting)$"),
                task_selector,
            ),
        ],
        SUMMARIZE_PAPER: [
            MessageHandler(
                filters.Document and ~(filters.COMMAND | filters.Regex("^End|end$")),
                summarize_paper,
            ),
        ],
        BRAINSTORM: [
            MessageHandler(
                filters.TEXT & ~(filters.COMMAND | filters.Regex("^End|end$")),
                brainstorm_a_paper,
            ),
        ],
        ASSISTANT: [
            MessageHandler(
                filters.VOICE & ~(filters.COMMAND | filters.Regex("^End|end$")),
                listen_and_speak,
            ),
        ],
    },
    fallbacks=[MessageHandler(filters.Regex("^End|end$"), end)],
    name="my_conv",
    persistent=True,
)

help_handler = CommandHandler("help", help_user)
