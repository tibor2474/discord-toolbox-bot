"""Server assets, icons, banners, and emoji commands."""

import discord
from discord import app_commands
from discord.ext import commands

from config import BOT_COLOR
from utils.image_embed import build_image_embed


class Server(commands.Cog):
    """Cog for server-related asset and media commands."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="servericon", description="Show server icon")
    @app_commands.guild_only()
    async def guild_icon(self, interaction: discord.Interaction) -> None:
        """Displays the server's icon in various image formats."""
        guild = interaction.guild
        if guild is None or guild.icon is None:
            await interaction.response.send_message(
                "This server doesn't have an icon",
                ephemeral=True
            )
            return

        embed = build_image_embed(guild.icon, title="Server icon", color=BOT_COLOR)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="serverbanner", description="Show server banner image")
    @app_commands.guild_only()
    async def guild_banner(self, interaction: discord.Interaction) -> None:
        """Displays the server's banner image if available."""
        guild = interaction.guild
        if guild is None or guild.banner is None:
            await interaction.response.send_message(
                "This server doesn't have a banner",
                ephemeral=True
            )
            return

        embed = build_image_embed(guild.banner, title="Server banner", color=BOT_COLOR)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="serverbackground", description="Show server invite background")
    @app_commands.guild_only()
    async def guild_invite_background(self, interaction: discord.Interaction) -> None:
        """Displays the server's invite splash background."""
        guild = interaction.guild
        if guild is None or guild.splash is None:
            await interaction.response.send_message(
                "This server doesn't have an invite background",
                ephemeral=True
            )
            return

        embed = build_image_embed(
            guild.splash,
            title="Server invite background",
            color=BOT_COLOR,
            include_gif=False,
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="serveremojis", description="Show server emojis")
    @app_commands.guild_only()
    async def guild_emojis(self, interaction: discord.Interaction) -> None:
        """Displays all custom emojis available in the server."""
        guild = interaction.guild
        if guild is None:
            await interaction.response.send_message(
                "This command can only be used in a server.",
                ephemeral=True
            )
            return

        emojis = [str(x) for x in guild.emojis]
        if not emojis:
            await interaction.response.send_message(
                "This server doesn't have any custom emojis",
                ephemeral=True
            )
            return

        embed = discord.Embed(color=BOT_COLOR, description=" ".join(emojis), title="Server emojis")
        embed.set_footer(text=f"{len(emojis)} emojis total")
        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    """Extension setup entry point."""
    await bot.add_cog(Server(bot))
