"""Configuration settings and asset definitions for the Toolbox Discord bot."""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Authentication
BOT_TOKEN = os.getenv("TOKEN")  # Bot token from environment / secrets file

BOT_COLOR = 0xb4befe  # Embed accent color
