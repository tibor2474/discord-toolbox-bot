import os
from dotenv import load_dotenv
load_dotenv()

bot_token = os.getenv("TOKEN")
bot_time = "%d/%b/%Y %H:%M:%S"
bot_color = 0x313244

# ICONS
member_icon = ""
server_icon = ""
channel_icon = ""
role_icon = ""
image_icon = ""