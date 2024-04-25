import time

from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.speech2text import speech_to_text


async def speech_to_text_audio(
    user_voice,
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    SALUTE_AUTH_DATA,
    SALUTE_SCOPE,
):
    TOKEN = await speech_to_text.get_new_token(
        update=update,
        context=context,
        AUTH_DATA=SALUTE_AUTH_DATA,
        API_SCOPE=SALUTE_SCOPE,
    )
    request_file_id = await speech_to_text.speech_to_text(user_voice, TOKEN)
    task_id = await speech_to_text.speech_recognition_task(request_file_id, TOKEN)
    time.sleep(10)
    response = await speech_to_text.get_task_status(task_id, TOKEN)
    Data = await speech_to_text.get_the_text(response, TOKEN)
    return Data
