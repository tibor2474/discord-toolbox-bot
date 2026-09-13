"""Configuration settings and asset definitions for the Toolbox Discord bot."""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Authentication
BOT_TOKEN = os.getenv("TOKEN")  # Bot token from environment / secrets file

# Formatting and theming
BOT_TIME = "%d/%b/%Y %H:%M:%S"  # Time format string
BOT_COLOR = 0xb4befe  # Embed accent color

# CDN and UI Icons (Source: FontAwesome)
MEMBER_ICON = "https://i.imgur.com/c7DXPqC.png"
SERVER_ICON = "https://i.imgur.com/0BvjJ7g.png"
CHANNEL_ICON = "https://i.imgur.com/0BvjJ7g.png"
ROLE_ICON = "https://i.imgur.com/0BvjJ7g.png"
MESSAGE_ICON = "https://i.imgur.com/LlJFaux.png"
IMAGE_ICON = "https://i.imgur.com/gNanKO7.png"
X_ICON = "https://i.imgur.com/jHfMoVb.png"
EMOJI_ICON = "https://i.imgur.com/N29kBBc.png"
LINK_ICON = "https://i.imgur.com/cLBbPuJ.png"
