"""Main entry point for the Toolbox Discord bot.

Configures dual UTC logging (console and timestamped file under logs/),
initializes the bot with Discord.py v2, loads cogs, and configures error handling.
"""

import logging
import os
import sys
import time

import discord
from discord import app_commands
from discord.ext import commands

from config import BOT_TOKEN

# ==============================================================================
# Logging Configuration
# ==============================================================================

# Ensure logs directory exists
log_dir = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(log_dir, exist_ok=True)

# Generate timestamped log filename (UTC)
log_timestamp = discord.utils.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
log_filepath = os.path.join(log_dir, f"bot_{log_timestamp}.log")

# Standard format using UTC time
log_formatter = logging.Formatter(
    fmt="[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log_formatter.converter = time.gmtime

# Console handler (stdout)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(log_formatter)
console_handler.setLevel(logging.INFO)

# File handler (logs/bot_<timestamp>.log)
file_handler = logging.FileHandler(log_filepath, encoding="utf-8")
file_handler.setFormatter(log_formatter)
file_handler.setLevel(logging.INFO)

# Configure root logger
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
root_logger.addHandler(console_handler)
root_logger.addHandler(file_handler)

logger = logging.getLogger("discord.app")


# ==============================================================================
# Bot Class Definition
# ==============================================================================

class ToolboxBot(commands.Bot):
    """Toolbox Discord Bot managing cogs and application command trees."""

    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.members = True
        intents.presences = True

        super().__init__(
            command_prefix=commands.when_mentioned_or("!"),
            intents=intents,
            help_command=None,
        )

    async def setup_hook(self) -> None:
        """Asynchronous setup hook executed prior to login.

        Loads all extensions from the cogs/ directory and syncs the app command tree.
        """
        # Load extensions from cogs directory
        for filename in sorted(os.listdir("./cogs")):
            if filename.endswith(".py"):
                extension = f"cogs.{filename[:-3]}"
                try:
                    await self.load_extension(extension)
                    logger.info("Loaded %s", filename)
                except Exception as error:
                    logger.error("ERROR %s could not be loaded: %s", filename, error, exc_info=True)

        # Synchronize application command tree with Discord
        try:
            synced = await self.tree.sync()
            logger.info("Synced %d application commands", len(synced))
        except Exception as error:
            logger.error("Failed to sync application commands: %s", error, exc_info=True)


bot = ToolboxBot()


# ==============================================================================
# Event Listeners
# ==============================================================================

@bot.event
async def on_ready() -> None:
    """Invoked when the bot has successfully established a gateway connection."""
    logger.info("Logged in as %s (ID: %s)", bot.user, bot.user.id if bot.user else "Unknown")


@bot.listen("on_message")
async def on_message(message: discord.Message) -> None:
    """Listener for incoming messages."""
    if message.author == bot.user:
        return


@bot.listen("on_interaction")
async def on_interaction(interaction: discord.Interaction) -> None:
    """Logs application command executions."""
    if interaction.type == discord.InteractionType.application_command:
        command_name = interaction.command.name if interaction.command else "unknown"
        user = interaction.user
        logger.info("User @%s (ID:%s) used the %s command", user.name, user.id, command_name)


# ==============================================================================
# Error Handling
# ==============================================================================

@bot.tree.error
async def on_app_command_error(
    interaction: discord.Interaction,
    error: app_commands.AppCommandError
) -> None:
    """Global error handler for application commands."""
    command_name = interaction.command.name if interaction.command else "unknown"
    logger.error("Error executing command '%s': %s", command_name, error, exc_info=error)

    # Unwrap original error if wrapped in CommandInvokeError
    original_error = getattr(error, "original", error)

    if (
        isinstance(error, app_commands.BotMissingPermissions)
        or isinstance(original_error, commands.BotMissingPermissions)
    ):
        response_text = "I don't have the correct permissions to do that."
    elif (
        isinstance(error, app_commands.MissingPermissions)
        or isinstance(original_error, commands.MissingPermissions)
    ):
        response_text = "You don't have the correct permissions to do that."
    elif isinstance(error, app_commands.CheckFailure):
        response_text = "You do not meet the requirements to execute this command."
    else:
        response_text = "An error occurred while executing the command."

    try:
        if interaction.response.is_done():
            await interaction.followup.send(response_text, ephemeral=True)
        else:
            await interaction.response.send_message(response_text, ephemeral=True)
    except Exception as send_err:
        logger.error("Failed to deliver error response: %s", send_err)


# ==============================================================================
# Bot Runner
# ==============================================================================

def main() -> None:
    """Validates configuration and launches the bot."""
    if not BOT_TOKEN:
        logger.critical(
            "No bot token provided! Please define the TOKEN environment variable in your secrets."
        )
        sys.exit(1)

    # Pass log_handler=None to retain our custom logging configuration
    bot.run(BOT_TOKEN, log_handler=None)


if __name__ == "__main__":
    main()
