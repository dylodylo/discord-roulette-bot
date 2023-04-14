import os

from dotenv import load_dotenv
from interactions import Client


def initialize_bot():
    load_dotenv()
    bot_token = os.environ.get("BOT_TOKEN")
    bot = Client(token=bot_token)
    bot.load("roulette_commands")
    bot.start()
    print("BOT IS ACTIVE")
