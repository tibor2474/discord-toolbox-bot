"""Configuration settings and asset definitions for the Toolbox Discord bot."""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Authentication
BOT_TOKEN = os.getenv("TOKEN")  # Bot token from environment / secrets file

_color_env = os.getenv("BOT_COLOR")
BOT_COLOR = int(_color_env.lstrip("#"), 16) if _color_env else 0xb4befe  # Embed accent color
