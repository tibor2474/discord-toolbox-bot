"""Thread management and moderation commands."""

import discord
from discord import app_commands
from discord.ext import commands


class Thread(commands.Cog):
    """Cog for thread management commands."""

    thread = app_commands.Group(name="thread", description="Thread management commands")

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @thread.command(
        name="close",
        description="Allows a staff member or the thread owner to close the thread"
    )
    @app_commands.guild_only()
    @app_commands.checks.bot_has_permissions(manage_threads=True)
    @app_commands.describe(lock="Lock thread?")
    async def thread_close(self, interaction: discord.Interaction, lock: bool = False) -> None:
        """Closes and optionally locks the current thread."""
        if not isinstance(interaction.channel, discord.Thread):
            await interaction.response.send_message(
                "This command can only be used in threads.",
                ephemeral=True
            )
            return

        assert isinstance(interaction.user, discord.Member)
        if interaction.channel.permissions_for(interaction.user).manage_threads:
            if lock:
                await interaction.response.send_message(
                    "This thread was archived and locked by a staff member."
                )
            else:
                await interaction.response.send_message(
                    "This thread was archived by a staff member."
                )
            await interaction.channel.edit(
                archived=True,
                locked=lock,
                reason=f"Action by @{interaction.user.name} ({interaction.user.id})"
            )

        elif interaction.user.id == interaction.channel.owner_id:
            await interaction.response.send_message(
                "This thread was archived by the user that opened it."
            )
            await interaction.channel.edit(
                archived=True,
                reason=f"Action by @{interaction.user.name} ({interaction.user.id})"
            )

        else:
            await interaction.response.send_message(
                "This command can only be used by the owner of the thread or a staff member.",
                ephemeral=True
            )

    @thread.command(
        name="open",
        description="Reopen an archived thread"
    )
    @app_commands.guild_only()
    @app_commands.checks.bot_has_permissions(manage_threads=True)
    @app_commands.describe(thread_id="ID of the archived thread (defaults to this thread)")
    async def thread_open(self, interaction: discord.Interaction, thread_id: str | None = None) -> None:
        """Reopens and unlocks the current thread or the thread with the given ID."""
        thread: discord.Thread | None = None
        if thread_id is None:
            if isinstance(interaction.channel, discord.Thread):
                thread = interaction.channel
        else:
            try:
                channel_id = int(thread_id)
            except ValueError:
                await interaction.response.send_message(
                    "Thread ID must be a number.", ephemeral=True
                )
                return

            channel = interaction.guild.get_thread(channel_id) if interaction.guild else None
            if channel is None:
                try:
                    channel = await self.bot.fetch_channel(channel_id)
                except (discord.NotFound, discord.Forbidden, discord.HTTPException):
                    channel = None
            if isinstance(channel, discord.Thread):
                thread = channel

        if thread is None or thread.guild.id != interaction.guild_id:
            await interaction.response.send_message(
                "That is not a valid thread ID.", ephemeral=True
            )
            return

        assert isinstance(interaction.user, discord.Member)
        is_staff = thread.permissions_for(interaction.user).manage_threads
        is_owner = interaction.user.id == thread.owner_id
        if not (is_staff or is_owner):
            await interaction.response.send_message(
                "This command can only be used by the owner of the thread or a staff member.",
                ephemeral=True
            )
            return

        await thread.edit(
            archived=False,
            locked=False,
            reason=f"Action by @{interaction.user.name} ({interaction.user.id})"
        )
        await interaction.response.send_message("Reopened thread.")

    @thread.command(name="rename", description="Change the name of the thread")
    @app_commands.guild_only()
    @app_commands.checks.bot_has_permissions(manage_threads=True)
    @app_commands.describe(name="New name for this thread")
    async def thread_name(self, interaction: discord.Interaction, name: app_commands.Range[str, 1, 100]) -> None:
        """Renames the current thread."""
        if not isinstance(interaction.channel, discord.Thread):
            await interaction.response.send_message(
                "This command can only be used in threads.",
                ephemeral=True
            )
            return

        assert isinstance(interaction.user, discord.Member)
        can_manage = (
            interaction.channel.permissions_for(interaction.user).manage_threads
            or interaction.user.id == interaction.channel.owner_id
        )
        if can_manage:
            await interaction.response.defer()
            try:
                await interaction.channel.edit(
                    name=name,
                    reason=f"Action by @{interaction.user.name} ({interaction.user.id})"
                )
            except (discord.HTTPException, discord.RateLimited):
                await interaction.followup.send(
                    "Discord limits each thread to two name changes every 10 minutes. Please try again later.",
                    ephemeral=True
                )
                return
            await interaction.followup.send(f"Changed thread name to: **{name}**")
        else:
            await interaction.response.send_message(
                "This command can only be used by the owner of the thread or a staff member.",
                ephemeral=True
            )

    @thread.command(name="slowmode", description="Set custom slowmode for a thread")
    @app_commands.guild_only()
    @app_commands.default_permissions(manage_channels=True)
    @app_commands.checks.bot_has_permissions(manage_threads=True)
    @app_commands.describe(seconds="Slowmode delay in seconds (set to 0 to disable)")
    async def thread_slowmode(self, interaction: discord.Interaction, seconds: app_commands.Range[int, 0, 21600]) -> None:
        """Sets slowmode delay in seconds for the current thread."""
        if not isinstance(interaction.channel, discord.Thread):
            await interaction.response.send_message(
                "This command can only be used in threads.",
                ephemeral=True
            )
            return

        channel = interaction.channel
        await channel.edit(
            slowmode_delay=seconds,
            reason=f"Action by @{interaction.user.name} ({interaction.user.id})"
        )

        if seconds == 0:
            await interaction.response.send_message("Disabled slowmode")
            return
        await interaction.response.send_message(f"Changed slowmode to {seconds} seconds")


async def setup(bot: commands.Bot) -> None:
    """Extension setup entry point."""
    await bot.add_cog(Thread(bot))
