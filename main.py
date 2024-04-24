import logging
from bot import initialize_the_bot as init, handlers

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

if __name__ == "__main__":
    app = init()
    app.add_handler(handlers.conv_handler)
    app.add_handler(handlers.help_handler)
    app.run_polling()
