import discord
from discord import app_commands
from discord.ext import commands


class Thread(commands.Cog):
    """Cog for thread management commands."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="threadclose",
        description="Allows a staff member or the thread owner to close the thread"
    )
    @app_commands.guild_only()
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
                await interaction.response.send_message("This thread was archived and locked by a staff member.")
            else:
                await interaction.response.send_message("This thread was archived by a staff member.")
            await interaction.channel.edit(archived=True, locked=lock)

        elif interaction.user.id == interaction.channel.owner_id:
            await interaction.response.send_message("This thread was archived by the user that opened it.")
            await interaction.channel.edit(archived=True)

        else:
            await interaction.response.send_message(
                "This command can only be used by the owner of the thread or a staff member.",
                ephemeral=True
            )

    @app_commands.command(name="threadname", description="Change the name of the thread")
    @app_commands.guild_only()
    @app_commands.describe(name="New name for this thread")
    async def thread_name(self, interaction: discord.Interaction, name: str) -> None:
        """Renames the current thread."""
        if not isinstance(interaction.channel, discord.Thread):
            await interaction.response.send_message(
                "This command can only be used in threads.",
                ephemeral=True
            )
            return

        assert isinstance(interaction.user, discord.Member)
        if interaction.channel.permissions_for(interaction.user).manage_threads or interaction.user.id == interaction.channel.owner_id:
            await interaction.channel.edit(name=name)
            await interaction.response.send_message(f"Changed thread name to: **{name}**")
        else:
            await interaction.response.send_message(
                "This command can only be used by the owner of the thread or a staff member.",
                ephemeral=True
            )

    @app_commands.command(name="threadslowmode", description="Set custom slowmode for a thread")
    @app_commands.guild_only()
    @app_commands.default_permissions(manage_channels=True)
    @app_commands.describe(seconds="Slowmode delay in seconds (set to 0 to disable)")
    async def thread_slowmode(self, interaction: discord.Interaction, seconds: int) -> None:
        """Sets slowmode delay in seconds for the current thread."""
        if not isinstance(interaction.channel, discord.Thread):
            await interaction.response.send_message(
                "This command can only be used in threads.",
                ephemeral=True
            )
            return

        channel = interaction.channel
        await channel.edit(slowmode_delay=seconds)

        if seconds == 0:
            await interaction.response.send_message("Disabled slowmode")
            return
        await interaction.response.send_message(f"Changed slowmode to {seconds} seconds")


async def setup(bot: commands.Bot) -> None:
    """Extension setup entry point."""
    await bot.add_cog(Thread(bot))
