import time

from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.text2speech import text_to_speech


async def text_to_speech_impl(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    SALUTE_AUTH_DATA,
    SALUTE_SCOPE,
):
    TOKEN = await text_to_speech.get_new_token(
        update=update,
        context=context,
        AUTH_DATA=SALUTE_AUTH_DATA,
        API_SCOPE=SALUTE_SCOPE,
    )

    request_file_id = await text_to_speech.text_to_speech(update.message.text, TOKEN)
    task_id = await text_to_speech.speech_recognition_task(request_file_id, TOKEN)
    time.sleep(30)

    response = await text_to_speech.get_task_status(task_id, TOKEN)
    time.sleep(6)
    Data = await text_to_speech.get_the_audio(response, TOKEN)
    return Data
