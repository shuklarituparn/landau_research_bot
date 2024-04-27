import os
import resend
from dotenv import load_dotenv

load_dotenv()

RESEND_API_KEY = os.getenv("RESEND_API_KEY")


def send_mail(email_to: str, texttosend: str):
    resend.api_key = RESEND_API_KEY

    params = {
        "from": "Gigachat Assistant <gigachat@rtprnshukla.ru>",
        "to": [f"{email_to}"],
        "subject": "Вот что вы искали!",
        "html": "<strong>Вот идеи для вашей научной работы!</strong>"
        + f"<p>{texttosend}</p>",
    }
    resend.Emails.send(params)
