"""Server assets, icons, banners, and emoji commands."""

import discord
from discord import app_commands
from discord.ext import commands

from config import BOT_COLOR


class Server(commands.Cog):
    """Cog for server-related asset and media commands."""

    server = app_commands.Group(name="server", description="Server information and assets")

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @server.command(name="icon", description="Show server icon")
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

        png = guild.icon.replace(format="png")
        jpg = guild.icon.replace(format="jpg")
        webp = guild.icon.replace(format="webp")
        gif = guild.icon.replace(format="gif") if guild.icon.is_animated() else None

        desc = (
            f"[PNG]({png}) - [JPG]({jpg}) - [WEBP]({webp}) - [GIF]({gif})"
            if gif
            else f"[PNG]({png}) - [JPG]({jpg}) - [WEBP]({webp})"
        )

        embed = discord.Embed(description=desc, color=BOT_COLOR, title="Server icon")
        embed.set_image(url=guild.icon.url)
        await interaction.response.send_message(embed=embed)

    @server.command(name="banner", description="Show server banner image")
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

        png = guild.banner.replace(format="png")
        jpg = guild.banner.replace(format="jpg")
        webp = guild.banner.replace(format="webp")
        gif = guild.banner.replace(format="gif") if guild.banner.is_animated() else None

        desc = (
            f"[PNG]({png}) - [JPG]({jpg}) - [WEBP]({webp}) - [GIF]({gif})"
            if gif
            else f"[PNG]({png}) - [JPG]({jpg}) - [WEBP]({webp})"
        )

        embed = discord.Embed(description=desc, color=BOT_COLOR, title="Server banner")
        embed.set_image(url=guild.banner.url)
        await interaction.response.send_message(embed=embed)

    @server.command(name="splash", description="Show server invite background")
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

        png = guild.splash.replace(format="png")
        jpg = guild.splash.replace(format="jpg")
        webp = guild.splash.replace(format="webp")

        embed = discord.Embed(
            description=f"[PNG]({png}) - [JPG]({jpg}) - [WEBP]({webp})",
            title="Server invite background",
            color=BOT_COLOR
        )
        embed.set_image(url=guild.splash.url)
        await interaction.response.send_message(embed=embed)

    @server.command(name="emojis", description="Show server emojis")
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

    @server.command(name="info", description="Show info about this server")
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(manage_guild=True)
    async def guild_info(self, interaction: discord.Interaction) -> None:
        """Displays detailed statistics and configuration for the current server."""
        info_cog = self.bot.get_cog("Info")
        if info_cog is None:
            await interaction.response.send_message(
                "Server information is currently unavailable.",
                ephemeral=True
            )
            return
        await info_cog._send_server_info(interaction)


async def setup(bot: commands.Bot) -> None:
    """Extension setup entry point."""
    await bot.add_cog(Server(bot))
