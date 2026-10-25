"""Channel management commands and configuration for the bot."""

from typing import Union
import discord
from discord import app_commands
from discord.ext import commands


class Channel(commands.Cog):
    """Cog for channel administration and configuration commands."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="slowmode", description="Set custom slowmode for a channel")
    @app_commands.guild_only()
    @app_commands.default_permissions(manage_channels=True)
    @app_commands.checks.bot_has_permissions(manage_channels=True)
    @app_commands.describe(
        channel="Select a channel (defaults to this channel)",
        seconds="Slowmode delay in seconds (set to 0 to disable)"
    )
    async def channel_slowmode(
        self,
        interaction: discord.Interaction,
        seconds: app_commands.Range[int, 0, 21600],
        channel: Union[discord.TextChannel, discord.StageChannel, discord.VoiceChannel, None] = None
    ) -> None:
        """Sets slowmode delay in seconds for the selected channel."""
        channel = channel if channel is not None else interaction.channel
        if not isinstance(channel, (discord.TextChannel, discord.StageChannel, discord.VoiceChannel)):
            await interaction.response.send_message(
                "This channel does not support this command. Select a supported channel.",
                ephemeral=True
            )
            return
        await channel.edit(
            slowmode_delay=seconds,
            reason=f"Action by @{interaction.user.name} ({interaction.user.id})"
        )
        if seconds == 0:
            await interaction.response.send_message(f"Disabled slowmode for {channel.mention}")
            return
        await interaction.response.send_message(
            f"Changed slowmode for {channel.mention} to {seconds} seconds"
        )

    @app_commands.command(
        name="nsfw",
        description="Turn on or off age-restricted mode for a channel"
    )
    @app_commands.guild_only()
    @app_commands.default_permissions(manage_channels=True)
    @app_commands.checks.bot_has_permissions(manage_channels=True)
    @app_commands.describe(
        channel="Select a channel (defaults to this channel)",
        mode="Turn on or off"
    )
    async def channel_nsfw(
        self,
        interaction: discord.Interaction,
        mode: bool,
        channel: Union[discord.TextChannel, discord.StageChannel, discord.VoiceChannel, discord.ForumChannel, None] = None
    ) -> None:
        """Toggles the age-restriction (NSFW) setting on a channel."""
        channel = channel if channel is not None else interaction.channel
        if not isinstance(channel, (discord.TextChannel, discord.StageChannel, discord.VoiceChannel, discord.ForumChannel)):
            await interaction.response.send_message(
                "This channel does not support this command. Select a supported channel.",
                ephemeral=True
            )
            return
        if mode:
            await channel.edit(
                nsfw=True,
                reason=f"Action by @{interaction.user.name} ({interaction.user.id})"
            )
            await interaction.response.send_message(
                f"Turned on age-restriction for {channel.mention}"
            )
        else:
            await channel.edit(
                nsfw=False,
                reason=f"Action by @{interaction.user.name} ({interaction.user.id})"
            )
            await interaction.response.send_message(
                f"Turned off age-restriction for {channel.mention}"
            )

    @app_commands.command(name="vclimit", description="Set user limit for voice channels")
    @app_commands.guild_only()
    @app_commands.default_permissions(manage_channels=True)
    @app_commands.checks.bot_has_permissions(manage_channels=True)
    @app_commands.describe(
        channel="Select a channel (defaults to this channel)",
        limit="User limit (set to 0 to disable)"
    )
    async def channel_limit(
        self,
        interaction: discord.Interaction,
        limit: app_commands.Range[int, 0, 99],
        channel: Union[discord.StageChannel, discord.VoiceChannel, None] = None
    ) -> None:
        """Sets the maximum user limit for a voice or stage channel."""
        channel = channel if channel is not None else interaction.channel
        if not isinstance(channel, (discord.StageChannel, discord.VoiceChannel)):
            await interaction.response.send_message(
                "This channel does not support this command. Select a supported channel.",
                ephemeral=True
            )
            return
        await channel.edit(
            user_limit=limit,
            reason=f"Action by @{interaction.user.name} ({interaction.user.id})"
        )
        if limit == 0:
            await interaction.response.send_message(f"Disabled user limit for {channel.mention}")
            return
        await interaction.response.send_message(
            f"Changed user limit for {channel.mention} to {limit} members"
        )

    REGION_CHOICES = [
        app_commands.Choice(name="Automatic", value="automatic"),
        app_commands.Choice(name="Brazil", value="brazil"),
        app_commands.Choice(name="Hong Kong", value="hongkong"),
        app_commands.Choice(name="India", value="india"),
        app_commands.Choice(name="Japan", value="japan"),
        app_commands.Choice(name="Rotterdam", value="rotterdam"),
        app_commands.Choice(name="Singapore", value="singapore"),
        app_commands.Choice(name="South Africa", value="southafrica"),
        app_commands.Choice(name="Sydney", value="sydney"),
        app_commands.Choice(name="US Central", value="us-central"),
        app_commands.Choice(name="US East", value="us-east"),
        app_commands.Choice(name="US South", value="us-south"),
        app_commands.Choice(name="US West", value="us-west"),
    ]

    @app_commands.command(name="vcregion", description="Change region for a voice channel")
    @app_commands.guild_only()
    @app_commands.default_permissions(manage_channels=True)
    @app_commands.checks.bot_has_permissions(manage_channels=True)
    @app_commands.describe(
        channel="Select a channel (defaults to this channel)",
        region="Select a region"
    )
    @app_commands.choices(region=REGION_CHOICES)
    async def channel_region(
        self,
        interaction: discord.Interaction,
        region: app_commands.Choice[str],
        channel: Union[discord.StageChannel, discord.VoiceChannel, None] = None
    ) -> None:
        """Changes the RTC voice region for a voice or stage channel."""
        channel = channel if channel is not None else interaction.channel
        if not isinstance(channel, (discord.StageChannel, discord.VoiceChannel)):
            await interaction.response.send_message(
                "This channel does not support this command. Select a supported channel.",
                ephemeral=True
            )
            return
        region_value = region.value
        set_region = None if region.value == "automatic" else region.value

        try:
            await channel.edit(
                rtc_region=set_region,
                reason=f"Action by @{interaction.user.name} ({interaction.user.id})"
            )
            await interaction.response.send_message(
                f"Changed region to {region_value} for {channel.mention}",
                ephemeral=True
            )
        except Exception:
            await interaction.response.send_message(
                f"Failed to change region for {channel.mention}",
                ephemeral=True
            )


async def setup(bot: commands.Bot) -> None:
    """Extension setup entry point."""
    await bot.add_cog(Channel(bot))
