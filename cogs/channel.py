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
    @app_commands.describe(
        channel="Select a channel",
        seconds="Slowmode delay in seconds (set to 0 to disable)"
    )
    async def channel_slowmode(
        self,
        interaction: discord.Interaction,
        channel: Union[discord.TextChannel, discord.StageChannel, discord.VoiceChannel],
        seconds: int
    ) -> None:
        """Sets slowmode delay in seconds for the selected channel."""
        await channel.edit(slowmode_delay=seconds)
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
    @app_commands.describe(
        channel="Select a channel",
        mode="Turn on or off"
    )
    async def channel_nsfw(
        self,
        interaction: discord.Interaction,
        channel: Union[
            discord.TextChannel, discord.StageChannel,
            discord.VoiceChannel, discord.ForumChannel
        ],
        mode: bool
    ) -> None:
        """Toggles the age-restriction (NSFW) setting on a channel."""
        if mode:
            await channel.edit(nsfw=True)
            await interaction.response.send_message(
                f"Turned on age-restriction for {channel.mention}"
            )
        else:
            await channel.edit(nsfw=False)
            await interaction.response.send_message(
                f"Turned off age-restriction for {channel.mention}"
            )

    @app_commands.command(name="vclimit", description="Set user limit for voice channels")
    @app_commands.guild_only()
    @app_commands.default_permissions(manage_channels=True)
    @app_commands.describe(
        channel="Select a channel",
        limit="User limit (set to 0 to disable)"
    )
    async def channel_limit(
        self,
        interaction: discord.Interaction,
        channel: Union[discord.StageChannel, discord.VoiceChannel],
        limit: int
    ) -> None:
        """Sets the maximum user limit for a voice or stage channel."""
        await channel.edit(user_limit=limit)
        if limit == 0:
            await interaction.response.send_message(f"Disabled user limit for {channel.mention}")
            return
        await interaction.response.send_message(
            f"Changed user limit for {channel.mention} to {limit} members"
        )

    REGION_CHOICES = [
        app_commands.Choice(name="Automatic", value="Automatic"),
        app_commands.Choice(name="Brazil", value="Brazil"),
        app_commands.Choice(name="Hong Kong", value="Hong Kong"),
        app_commands.Choice(name="India", value="India"),
        app_commands.Choice(name="Japan", value="Japan"),
        app_commands.Choice(name="Rotterdam", value="Rotterdam"),
        app_commands.Choice(name="Russia", value="Russia"),
        app_commands.Choice(name="Singapore", value="Singapore"),
        app_commands.Choice(name="South Africa", value="South Africa"),
        app_commands.Choice(name="Sydney", value="Sydney"),
        app_commands.Choice(name="US Central", value="US Central"),
        app_commands.Choice(name="US East", value="US East"),
        app_commands.Choice(name="US South", value="US South"),
        app_commands.Choice(name="US West", value="US West"),
    ]

    @app_commands.command(name="vcregion", description="Change region for a voice channel")
    @app_commands.guild_only()
    @app_commands.default_permissions(manage_channels=True)
    @app_commands.describe(
        channel="Select a channel",
        region="Select a region"
    )
    @app_commands.choices(region=REGION_CHOICES)
    async def channel_region(
        self,
        interaction: discord.Interaction,
        channel: Union[discord.StageChannel, discord.VoiceChannel],
        region: app_commands.Choice[str]
    ) -> None:
        """Changes the RTC voice region for a voice or stage channel."""
        region_value = region.value
        if region_value == "Automatic":
            set_region = None
        elif region_value == "Hong Kong":
            set_region = "hongkong"
        elif region_value == "South Africa":
            set_region = "southafrica"
        else:
            set_region = region_value.lower().replace(" ", "_")

        try:
            await channel.edit(
                rtc_region=set_region,
                reason=f"command executed by @{interaction.user.name}"
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
