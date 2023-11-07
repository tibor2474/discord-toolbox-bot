import os
from dotenv import load_dotenv
load_dotenv()

bot_token = os.getenv("TOKEN") # your token - set it in your secrets file
bot_time = "%d/%b/%Y %H:%M:%S" # time structure for logging
bot_color = 0xb4befe # embed color (#ffffff -> 0xffffff)

# ICONS
member_icon = "https://i.imgur.com/c7DXPqC.png"
server_icon = "https://i.imgur.com/0BvjJ7g.png"
channel_icon = "https://i.imgur.com/0BvjJ7g.png"
role_icon = "https://i.imgur.com/0BvjJ7g.png"
message_icon = "https://i.imgur.com/LlJFaux.png"
image_icon = "https://i.imgur.com/gNanKO7.png"
x_icon = "https://i.imgur.com/jHfMoVb.png"
emoji_icon = "https://i.imgur.com/N29kBBc.png"
link_icon = "https://i.imgur.com/cLBbPuJ.png"