"""Message inspection utilities and context menu commands."""

import discord
from discord import app_commands
from discord.ext import commands

from config import BOT_COLOR


@app_commands.context_menu(name="Show raw message")
@app_commands.guild_only()
async def raw_message(interaction: discord.Interaction, message: discord.Message) -> None:
    """Context menu command to display the raw content of a message."""
    if not message.content:
        await interaction.response.send_message(
            "The message doesn't have any content that I can show",
            ephemeral=True
        )
        return

    # Escape triple backticks so markdown codeblock does not break
    escaped_content = message.content.replace("```", "ˋˋˋ")
    embed = discord.Embed(
        color=BOT_COLOR,
        title=f"Raw message | ID:{message.id}",
        description=f"```{escaped_content}```"
    )
    embed.set_footer(text="The formatting might be inaccurate if you're viewing code blocks")
    await interaction.response.send_message(embed=embed, ephemeral=True)


class Message(commands.Cog):
    """Cog for message-related commands and context menus."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def cog_load(self) -> None:
        """Register the message context menu upon cog load."""
        self.bot.tree.add_command(raw_message)

    async def cog_unload(self) -> None:
        """Unregister the message context menu upon cog unload."""
        self.bot.tree.remove_command(raw_message.name, type=raw_message.type)


async def setup(bot: commands.Bot) -> None:
    """Extension setup entry point."""
    await bot.add_cog(Message(bot))
