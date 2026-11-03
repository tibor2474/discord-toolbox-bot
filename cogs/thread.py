"""Thread management and moderation commands."""

import discord
from discord import app_commands
from discord.ext import commands


class Thread(commands.Cog):
    """Cog for thread management commands."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def _resolve_thread(
        self, interaction: discord.Interaction, thread_id: str | None
    ) -> discord.Thread | None:
        """Returns the target thread or sends an error and returns None."""
        if thread_id is None:
            if isinstance(interaction.channel, discord.Thread):
                return interaction.channel
            await interaction.response.send_message(
                "This command can only be used in threads, or with a thread ID.",
                ephemeral=True
            )
            return None

        try:
            channel_id = int(thread_id)
        except ValueError:
            await interaction.response.send_message(
                "Thread ID must be a number.", ephemeral=True
            )
            return None

        channel = interaction.guild.get_thread(channel_id) if interaction.guild else None
        if channel is None:
            try:
                channel = await self.bot.fetch_channel(channel_id)
            except (discord.NotFound, discord.Forbidden, discord.HTTPException):
                channel = None

        if not isinstance(channel, discord.Thread) or channel.guild.id != interaction.guild_id:
            await interaction.response.send_message(
                "That is not a valid thread ID.", ephemeral=True
            )
            return None
        return channel

    @staticmethod
    def _thread_label(interaction: discord.Interaction, thread: discord.Thread) -> str:
        """Returns "This thread" when used in the thread itself, otherwise it'd mention it."""
        return "This thread" if interaction.channel_id == thread.id else thread.mention

    @app_commands.command(
        name="threadclose",
        description="Allows a staff member or the thread owner to close the thread"
    )
    @app_commands.guild_only()
    @app_commands.checks.bot_has_permissions(manage_threads=True)
    @app_commands.describe(
        lock="Lock thread?",
        thread_id="ID of the thread (defaults to this thread)"
    )
    async def thread_close(
        self, interaction: discord.Interaction, lock: bool = False, thread_id: str | None = None
    ) -> None:
        """Closes and optionally locks the current thread or the thread with the given ID."""
        thread = await self._resolve_thread(interaction, thread_id)
        if thread is None:
            return
        label = self._thread_label(interaction, thread)

        assert isinstance(interaction.user, discord.Member)
        if thread.permissions_for(interaction.user).manage_threads:
            if lock:
                await interaction.response.send_message(
                    f"**{label}** thread was archived and locked by a staff member."
                )
            else:
                await interaction.response.send_message(
                    f"**{label}** thread was archived by a staff member."
                )
            await thread.edit(
                archived=True,
                locked=lock,
                reason=f"Action by @{interaction.user.name} ({interaction.user.id})"
            )

        elif interaction.user.id == thread.owner_id:
            await interaction.response.send_message(
                f"**{label}** thread was archived by the user that opened it."
            )
            await thread.edit(
                archived=True,
                reason=f"Action by @{interaction.user.name} ({interaction.user.id})"
            )

        else:
            await interaction.response.send_message(
                "This command can only be used by the owner of the thread or a staff member.",
                ephemeral=True
            )

    @app_commands.command(
        name="threadopen",
        description="Reopen an archived thread"
    )
    @app_commands.guild_only()
    @app_commands.checks.bot_has_permissions(manage_threads=True)
    @app_commands.describe(thread_id="ID of the archived thread (defaults to this thread)")
    async def thread_open(
            self,
            interaction: discord.Interaction,
            thread_id: str | None = None
    ) -> None:
        """Reopens and unlocks the current thread or the thread with the given ID."""
        thread = await self._resolve_thread(interaction, thread_id)
        if thread is None:
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
        await interaction.response.send_message(f"Reopened {thread.mention}.")

    @app_commands.command(name="threadname", description="Change the name of the thread")
    @app_commands.guild_only()
    @app_commands.checks.bot_has_permissions(manage_threads=True)
    @app_commands.describe(
        name="New name for the thread",
        thread_id="ID of the thread (defaults to this thread)"
    )
    async def thread_name(
        self,
        interaction: discord.Interaction,
        name: app_commands.Range[str, 1, 100],
        thread_id: str | None = None
    ) -> None:
        """Renames the current thread or the thread with the given ID."""
        thread = await self._resolve_thread(interaction, thread_id)
        if thread is None:
            return

        assert isinstance(interaction.user, discord.Member)
        can_manage = (
            thread.permissions_for(interaction.user).manage_threads
            or interaction.user.id == thread.owner_id
        )
        if can_manage:
            await interaction.response.defer()
            try:
                await thread.edit(
                    name=name,
                    reason=f"Action by @{interaction.user.name} ({interaction.user.id})"
                )
            except (discord.HTTPException, discord.RateLimited):
                await interaction.followup.send(
                    "Discord limits each thread to two name changes every 10 minutes. "
                    "Please try again later.",
                    ephemeral=True
                )
                return
            await interaction.followup.send(f"Changed thread name to: **{name}**")
        else:
            await interaction.response.send_message(
                "This command can only be used by the owner of the thread or a staff member.",
                ephemeral=True
            )

    @app_commands.command(name="threadslowmode", description="Set custom slowmode for a thread")
    @app_commands.guild_only()
    @app_commands.default_permissions(manage_threads=True)
    @app_commands.checks.bot_has_permissions(manage_threads=True)
    @app_commands.describe(
        seconds="Slowmode delay in seconds (set to 0 to disable)",
        thread_id="ID of the thread (defaults to this thread)"
    )
    async def thread_slowmode(
        self,
        interaction: discord.Interaction,
        seconds: app_commands.Range[int, 0, 21600],
        thread_id: str | None = None
    ) -> None:
        """Sets slowmode delay in seconds for the current thread or the thread with the given ID."""
        thread = await self._resolve_thread(interaction, thread_id)
        if thread is None:
            return

        # default_permissions only covers the invoking channel, so check the target thread too
        assert isinstance(interaction.user, discord.Member)
        if not thread.permissions_for(interaction.user).manage_threads:
            await interaction.response.send_message(
                "You need the Manage Threads permission for that thread.",
                ephemeral=True
            )
            return

        await thread.edit(
            slowmode_delay=seconds,
            reason=f"Action by @{interaction.user.name} ({interaction.user.id})"
        )

        if seconds == 0:
            await interaction.response.send_message(f"Disabled slowmode in {thread.mention}")
            return
        await interaction.response.send_message(
            f"Changed slowmode in {thread.mention} to {seconds} seconds"
        )


async def setup(bot: commands.Bot) -> None:
    """Extension setup entry point."""
    await bot.add_cog(Thread(bot))
