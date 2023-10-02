import os
from dotenv import load_dotenv
load_dotenv()

bot_token = os.getenv("TOKEN")
bot_time = "%d/%b/%Y %H:%M:%S"