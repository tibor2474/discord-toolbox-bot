"""Configuration settings and asset definitions for the Toolbox Discord bot."""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Authentication
BOT_TOKEN = os.getenv("TOKEN")  # Bot token from environment / secrets file

_color_env = os.getenv("BOT_COLOR")
if _color_env:
    _color_value = _color_env.removeprefix("#")
    try:
        BOT_COLOR = int(_color_value, 16)
    except ValueError as error:
        raise ValueError(
            "BOT_COLOR must be a 6-digit hexadecimal color, for example '#b4befe'."
        ) from error
    if len(_color_value) != 6 or BOT_COLOR > 0xFFFFFF:
        raise ValueError(
            "BOT_COLOR must be a 6-digit hexadecimal color, for example '#b4befe'."
        )
else:
    BOT_COLOR = 0xb4befe  # Embed accent color
