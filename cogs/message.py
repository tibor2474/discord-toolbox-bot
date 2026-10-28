"""Message inspection utilities and context menu commands."""

import io
import json

import discord
from discord import app_commands
from discord.ext import commands

from config import BOT_COLOR


def format_raw_message(message: discord.Message) -> str:
    """Collect text, attachment URLs, and complete embed data for inspection."""
    sections = []
    if message.content:
        sections.append(message.content)
    if message.attachments:
        sections.append("Attachments:\n" + "\n".join(
            f"{attachment.filename}: {attachment.url}"
            for attachment in message.attachments
        ))
    if message.embeds:
        sections.append("Embeds:\n" + json.dumps(
            [embed.to_dict() for embed in message.embeds],
            ensure_ascii=False,
            indent=2,
        ))
    return "\n\n".join(sections)


@app_commands.context_menu(name="Show raw message")
@app_commands.guild_only()
async def raw_message(interaction: discord.Interaction, message: discord.Message) -> None:
    """Display raw message content, uploading long output as a text file."""
    content = format_raw_message(message)
    if not content:
        await interaction.response.send_message(
            "The message doesn't have any content that I can show",
            ephemeral=True
        )
        return

    # Escape triple backticks so markdown codeblock does not break
    escaped_content = content.replace("```", "ˋˋˋ")
    description = f"```{escaped_content}```"
    # Discord counts UTF-16 code units toward its 4096-character limit.
    if len(description.encode("utf-16-le")) // 2 > 4096:
        await interaction.response.send_message(
            "The raw message is too long to display; it is attached as a text file.",
            file=discord.File(
                io.BytesIO(content.encode("utf-8")),
                filename=f"raw-message-{message.id}.txt",
            ),
            ephemeral=True,
        )
        return

    embed = discord.Embed(
        color=BOT_COLOR,
        title=f"Raw message | ID:{message.id}",
        description=description
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
