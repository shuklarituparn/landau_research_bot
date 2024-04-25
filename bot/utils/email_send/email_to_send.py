import os
import resend
from dotenv import load_dotenv

load_dotenv()

RESEND_API_KEY = os.getenv("RESEND_API_KEY")


def send_mail(email_to: str, subject: str, texttosend: str):
    resend.api_key = RESEND_API_KEY

    params = {
        "from": "Gigachat Assistant <gigachat@rtprnshukla.ru>",
        "to": [f"{email_to}"],
        "subject": f"{subject}",
        "html": "<strong>Вот идеи для вашей научной работы!</strong>"
        + f"<p>{texttosend}</p>",
    }

    # Ensure you are using the correct method provided by the resend module
    # For example, if resend provides a `send_email()` method, use that instead.
    resend.Emails.send(params)
    # print(email)  everything works (as of now)

    # i can pass this function as  a tool for the helper function


# if __name__=="__main__":
#      send_mail("shukla.r@phystech.edu","testing phase", "JUST TESTING THAT EVERYTHING WORKS AND IS NOT A SHOWOFFQ")
