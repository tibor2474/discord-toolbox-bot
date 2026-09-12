from typing import Union
import discord
from discord import app_commands
from discord.ext import commands

from config import bot_color, image_icon, member_icon


class Members(commands.Cog):
    """Cog for member actions, avatars, banners, and member context menu."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.ctx_menu = app_commands.ContextMenu(
            name="Show info",
            callback=self.info_member_context,
        )
        self.ctx_menu.default_permissions = discord.Permissions(kick_members=True)
        self.ctx_menu.guild_only = True

    async def cog_load(self) -> None:
        """Register the user context menu upon cog load."""
        self.bot.tree.add_command(self.ctx_menu)

    async def cog_unload(self) -> None:
        """Unregister the user context menu upon cog unload."""
        self.bot.tree.remove_command(self.ctx_menu.name, type=self.ctx_menu.type)

    async def info_member_context(self, interaction: discord.Interaction, member: discord.Member) -> None:
        """Context menu command to display comprehensive member information."""
        creation_time = int(member.created_at.timestamp())
        join_time = int(member.joined_at.timestamp()) if member.joined_at else 0

        embed = discord.Embed(color=bot_color)
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_author(name="Member info", icon_url=member_icon)
        embed.add_field(name="User mention", value=member.mention, inline=True)
        embed.add_field(name="User name", value=member.name, inline=True)
        embed.add_field(name="Nickname", value=member.nick or "*None*", inline=True)

        embed.add_field(name="Server booster", value=bool(member.premium_since), inline=True)
        embed.add_field(name="In voice", value=bool(member.voice), inline=True)
        embed.add_field(name="Timed out", value=member.is_timed_out(), inline=True)

        if member.activity is not None:
            embed.add_field(name="Activity", value=str(member.activity), inline=False)
        else:
            embed.add_field(name="Activity", value="*None/hidden or offline*", inline=False)

        embed.add_field(name="Bot", value=member.bot, inline=True)
        embed.add_field(name="Status", value=str(member.status), inline=True)
        embed.add_field(name="User ID", value=f"||{member.id}||", inline=True)

        embed.add_field(name="Account created", value=f"<t:{creation_time}:R>", inline=True)
        embed.add_field(name="Joined server", value=f"<t:{join_time}:R>", inline=True)
        await interaction.response.send_message(embed=embed, ephemeral=True)

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

        embed = discord.Embed(description=desc, color=bot_color)
        embed.set_author(name=f"{member.display_name}'s avatar", icon_url=image_icon)
        embed.set_image(url=avatar.url)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="serveravatar", description="Show someone's server avatar")
    @app_commands.guild_only()
    @app_commands.describe(member="Select a user")
    async def member_guild_avatar(self, interaction: discord.Interaction, member: discord.Member) -> None:
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

            embed = discord.Embed(description=desc, color=bot_color)
            embed.set_author(name=f"{member.display_name}'s server avatar", icon_url=image_icon)
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

            embed = discord.Embed(description=desc, color=bot_color)
            embed.set_author(name=f"{member.name}'s banner", icon_url=member_icon)
            embed.set_image(url=banner.url)
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(
                f"{member.name} doesn't have a banner",
                ephemeral=True
            )

    @app_commands.command(name="vcmove", description="Move member to a different voice channel")
    @app_commands.guild_only()
    @app_commands.default_permissions(move_members=True)
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
            await member.move_to(channel, reason=f"command executed by @{interaction.user.name}")
            await interaction.response.send_message(
                f"Moved {member.mention} to {channel.mention}",
                ephemeral=True
            )


async def setup(bot: commands.Bot) -> None:
    """Extension setup entry point."""
    await bot.add_cog(Members(bot))