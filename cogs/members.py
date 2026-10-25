"""Member management commands, avatars, banners, and context menu actions."""

from typing import Union
import discord
from discord import app_commands
from discord.ext import commands

from config import BOT_COLOR
from utils.member_embed import build_member_embed


@app_commands.context_menu(name="Show info")
@app_commands.guild_only()
@app_commands.default_permissions(kick_members=True)
async def info_member_context(
    interaction: discord.Interaction,
    member: discord.Member
) -> None:
    """Context menu command to display comprehensive member information."""
    embed = build_member_embed(member)
    await interaction.response.send_message(embed=embed, ephemeral=True)


class Members(commands.Cog):
    """Cog for member actions, avatars, banners, and member context menu."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def cog_load(self) -> None:
        """Register the user context menu upon cog load."""
        self.bot.tree.add_command(info_member_context)

    async def cog_unload(self) -> None:
        """Unregister the user context menu upon cog unload."""
        self.bot.tree.remove_command(info_member_context.name, type=info_member_context.type)

    @app_commands.command(name="avatar", description="Show someone's avatar")
    @app_commands.describe(member="Select a user")
    async def member_avatar(self, interaction: discord.Interaction, member: discord.Member) -> None:
        """Displays the specified member's avatar in various formats."""
        avatar = member.display_avatar
        png = avatar.replace(format="png")
        jpg = avatar.replace(format="jpg")
        webp = avatar.replace(format="webp")
        gif = avatar.replace(format="gif") if avatar.is_animated() else None

        desc = (
            f"[PNG]({png}) [JPG]({jpg}) [WEBP]({webp}) [GIF]({gif})"
            if gif
            else f"[PNG]({png}) - [JPG]({jpg}) - [WEBP]({webp})"
        )

        embed = discord.Embed(description=desc, color=BOT_COLOR, title=f"{member.display_name}'s avatar")
        embed.set_image(url=avatar.url)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="serveravatar", description="Show someone's server avatar")
    @app_commands.guild_only()
    @app_commands.describe(member="Select a user")
    async def member_guild_avatar(
        self,
        interaction: discord.Interaction,
        member: discord.Member
    ) -> None:
        """Displays the specified member's guild-specific avatar."""
        if member.guild_avatar is not None:
            avatar = member.guild_avatar
            png = avatar.replace(format="png")
            jpg = avatar.replace(format="jpg")
            webp = avatar.replace(format="webp")
            gif = avatar.replace(format="gif") if avatar.is_animated() else None

            desc = (
                f"[PNG]({png}) [JPG]({jpg}) [WEBP]({webp}) [GIF]({gif})"
                if gif
                else f"[PNG]({png}) - [JPG]({jpg}) - [WEBP]({webp})"
            )

            embed = discord.Embed(description=desc, color=BOT_COLOR, title=f"{member.display_name}'s server avatar")
            embed.set_image(url=avatar.url)
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(
                f"{member.display_name} doesn't have a server avatar",
                ephemeral=True
            )

    @app_commands.command(name="banner", description="Show someone's banner (if they have one)")
    @app_commands.describe(member="Select a user")
    async def member_banner(self, interaction: discord.Interaction, member: discord.Member) -> None:
        """Displays the specified user's profile banner if present."""
        await interaction.response.defer()
        user = await self.bot.fetch_user(member.id)
        if user.banner is not None:
            banner = user.banner
            png = banner.replace(format="png")
            jpg = banner.replace(format="jpg")
            webp = banner.replace(format="webp")
            gif = banner.replace(format="gif") if banner.is_animated() else None

            desc = (
                f"[PNG]({png}) [JPG]({jpg}) [WEBP]({webp}) [GIF]({gif})"
                if gif
                else f"[PNG]({png}) - [JPG]({jpg}) - [WEBP]({webp})"
            )

            embed = discord.Embed(description=desc, color=BOT_COLOR, title=f"{member.name}'s banner")
            embed.set_image(url=banner.url)
            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send(
                f"{member.name} doesn't have a banner",
                ephemeral=True
            )

    @app_commands.command(name="vcmove", description="Move member to a different voice channel")
    @app_commands.guild_only()
    @app_commands.default_permissions(move_members=True)
    @app_commands.checks.bot_has_permissions(move_members=True)
    @app_commands.describe(member="Select a member", channel="Select a channel")
    async def member_move(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        channel: Union[discord.VoiceChannel, discord.StageChannel]
    ) -> None:
        """Moves a connected voice member to another voice/stage channel."""
        if member.voice is None:
            await interaction.response.send_message(
                f"{member.mention} is not in a voice channel",
                ephemeral=True
            )
        else:
            await interaction.response.defer(ephemeral=True)
            await member.move_to(channel, reason=f"command executed by @{interaction.user.name}")
            await interaction.followup.send(
                f"Moved {member.mention} to {channel.mention}",
                ephemeral=True
            )


async def setup(bot: commands.Bot) -> None:
    """Extension setup entry point."""
    await bot.add_cog(Members(bot))
