import time

from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.text2speech import text_to_speech


async def text_to_speech_impl(
    filename,
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

    request_file_id = await text_to_speech.text_to_speech(filename, TOKEN)
    task_id = await text_to_speech.speech_recognition_task(request_file_id, TOKEN)
    time.sleep(30)  # 30 seconds works, rest anything times-out before the job is done

    response = await text_to_speech.get_task_status(task_id, TOKEN)
    Data = await text_to_speech.get_the_audio(response, TOKEN)
    return Data


# Todo: text to speech, instead of that just use some voice to test it, instead of audio using voice
# Todo: Now need to make a multi agent system
