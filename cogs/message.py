"""Message inspection utilities and context menu commands."""

import discord
from discord import app_commands
from discord.ext import commands

from config import BOT_COLOR


class Message(commands.Cog):
    """Cog for message-related commands and context menus."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.ctx_menu = app_commands.ContextMenu(
            name="Show raw message",
            callback=self.raw_message,
        )
        self.ctx_menu.guild_only = True

    async def cog_load(self) -> None:
        """Register the message context menu upon cog load."""
        self.bot.tree.add_command(self.ctx_menu)

    async def cog_unload(self) -> None:
        """Unregister the message context menu upon cog unload."""
        self.bot.tree.remove_command(self.ctx_menu.name, type=self.ctx_menu.type)

    async def raw_message(self, interaction: discord.Interaction, message: discord.Message) -> None:
        """Context menu command to display the raw content of a message."""
        if not message.content:
            await interaction.response.send_message(
                "The message doesn't have any content that I can show",
                ephemeral=True
            )
            return

        embed = discord.Embed(
            color=BOT_COLOR,
            title=f"Raw message | ID:{message.id}",
            description=f"```{message.content}```"
        )
        embed.set_footer(text="The formatting might be inaccurate if you're viewing code blocks")
        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    """Extension setup entry point."""
    await bot.add_cog(Message(bot))
