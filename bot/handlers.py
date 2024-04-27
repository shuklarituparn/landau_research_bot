import datetime
import os

from dotenv import load_dotenv
import bot.Database.database as db
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
from bot.utils.email_send import email_to_send
from bot.utils.translate_utils import email_formatter

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

keyboard = [["summarize", "brainstorm"], ["assistant"]]


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
    if update.message.text.startswith("email:"):
        if db.checking_user_exits(update.effective_user.id):

            if db.checking_user_email_exits(user_id=update.effective_user.id) == "":
                email = update.message.text.split(":")[1]
                userid = update.effective_user.id
                db.User.update(email=email).where(db.User.userid == userid).execute()
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="получил ваш email: " f"{email}",
                )
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Есл хотите получить резултать в данном email",
                )
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="отправьте текст в формате mail:{что вы хотите}",
                )
                print(email)  # email get
        else:
            email = update.message.text.split(":")[1]
            db.User.create(
                userid=update.effective_user.id,
                name=update.effective_user.first_name,
                username=update.effective_user.username,
                chromacollection="",
                email=email,
                usertoken="",
                gigachat_token="",
                lastGen=datetime.datetime.now(),
                last_gen_gigachat=datetime.datetime.now(),
            )
    elif update.message.text.startswith("mail:"):
        if db.checking_user_email_exits(user_id=update.effective_user.id) != "":
            email = db.User.get(userid=update.effective_user.id).email
            print(email)
            text_to_find = update.message.text.split(":")[1]
            print(text_to_find)
            doc_to_send = await brainstorm.generate_find_the_paper(
                user_query=text_to_find
            )
            # formatted_text=await email_formatter.text_formatter(doc_to_send)
            await context.bot.send_message(
                chat_id=update.effective_chat.id, text="чекните ваш mail"
            )
            email_to_send.send_mail(email_to=email, texttosend=doc_to_send)
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id, text="добавь mail"
            )

    elif update.message.text.startswith("nml:"):
        text_to_find = update.message.text.split(":")[1]
        print(text_to_find)
        doc = await brainstorm.generate_find_the_paper(user_query=text_to_find)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=doc)
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="nml: , email: , mail:"
        )


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
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Привет")
    result = await ai_helper.ai_help(update.message.text)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=result)


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
                filters.Regex("^(summarize|brainstorm|assistant)$"),
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
                filters.TEXT and ~(filters.COMMAND | filters.Regex("^End|end$")),
                ask_ai,
            ),
        ],
    },
    fallbacks=[MessageHandler(filters.Regex("^End|end$"), end)],
    name="my_conv",
    persistent=True,
)

help_handler = CommandHandler("help", help_user)
