"""Member management commands, avatars, banners, and context menu actions."""

from typing import Union
import discord
from discord import app_commands
from discord.ext import commands

from config import BOT_COLOR
from utils.member_embed import build_member_embed
from utils.image_embed import build_image_embed


@app_commands.context_menu(name="Show info")
@app_commands.guild_only()
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
    @app_commands.describe(member="Select a user (defaults to you)")
    async def member_avatar(
            self,
            interaction: discord.Interaction,
            member: discord.Member | None = None
    ) -> None:
        """Displays the specified member's avatar in various formats."""
        member = member if member is not None else interaction.user
        avatar = member.display_avatar
        embed = build_image_embed(
            avatar,
            title=f"{member.display_name}'s avatar",
            color=BOT_COLOR,
            gif_separator=" ",
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="serveravatar", description="Show someone's server avatar")
    @app_commands.guild_only()
    @app_commands.describe(member="Select a user (defaults to you)")
    async def member_guild_avatar(
        self,
        interaction: discord.Interaction,
        member: discord.Member | None = None
    ) -> None:
        """Displays the specified member's guild-specific avatar."""
        member = member if member is not None else interaction.user
        if member.guild_avatar is not None:
            avatar = member.guild_avatar
            embed = build_image_embed(
                avatar,
                title=f"{member.display_name}'s server avatar",
                color=BOT_COLOR,
                gif_separator=" ",
            )
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message(
                f"{member.display_name} doesn't have a server avatar",
                ephemeral=True
            )

    @app_commands.command(name="banner", description="Show someone's banner (if they have one)")
    @app_commands.describe(member="Select a user (defaults to you)")
    async def member_banner(
            self,
            interaction: discord.Interaction,
            member: discord.Member | None = None
    ) -> None:
        """Displays the specified user's profile banner if present."""
        member = member if member is not None else interaction.user
        await interaction.response.defer()
        user = await self.bot.fetch_user(member.id)
        if user.banner is not None:
            banner = user.banner
            embed = build_image_embed(
                banner,
                title=f"{member.name}'s banner",
                color=BOT_COLOR,
                gif_separator=" ",
            )
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
    @app_commands.describe(
        member="Select a member (defaults to you)",
        channel="Select a channel (defaults to this channel)"
    )
    async def member_move(
        self,
        interaction: discord.Interaction,
        member: discord.Member | None = None,
        channel: Union[discord.VoiceChannel, discord.StageChannel, None] = None
    ) -> None:
        """Moves a connected voice member to another voice/stage channel."""
        member = member if member is not None else interaction.user
        channel = channel if channel is not None else interaction.channel
        if not isinstance(channel, (discord.VoiceChannel, discord.StageChannel)):
            await interaction.response.send_message(
                "Select a voice or stage channel, or run this command in one.",
                ephemeral=True
            )
            return
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
