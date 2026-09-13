"""Configuration settings and asset definitions for the Toolbox Discord bot."""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Authentication
bot_token = os.getenv("TOKEN")  # Bot token from environment / secrets file

# Formatting and theming
bot_time = "%d/%b/%Y %H:%M:%S"  # Time format string
bot_color = 0xb4befe  # Embed accent color

# CDN and UI Icons (Source: FontAwesome)
member_icon = "https://i.imgur.com/c7DXPqC.png"
server_icon = "https://i.imgur.com/0BvjJ7g.png"
channel_icon = "https://i.imgur.com/0BvjJ7g.png"
role_icon = "https://i.imgur.com/0BvjJ7g.png"
message_icon = "https://i.imgur.com/LlJFaux.png"
image_icon = "https://i.imgur.com/gNanKO7.png"
x_icon = "https://i.imgur.com/jHfMoVb.png"
emoji_icon = "https://i.imgur.com/N29kBBc.png"
link_icon = "https://i.imgur.com/cLBbPuJ.png"
