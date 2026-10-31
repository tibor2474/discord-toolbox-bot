"""Permission inspection commands for members and roles."""

import discord
from discord import app_commands
from discord.ext import commands

from utils.permissions import build_permissions_embed


class Permission(commands.Cog):
    """Cog for viewing role and member permissions within the guild."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="memberpermissions", description="Show permissions for a member")
    @app_commands.guild_only()
    @app_commands.describe(member="Select a member (defaults to yourself if not specified)")
    async def show_member_perms(
        self,
        interaction: discord.Interaction,
        member: discord.Member | None = None
    ) -> None:
        """Displays all granted guild permissions for the specified member."""
        member = member if member is not None else interaction.user
        embed = build_permissions_embed(member)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="rolepermissions", description="Show permissions for a role")
    @app_commands.guild_only()
    @app_commands.describe(role="Select a role")
    async def show_role_perms(
        self,
        interaction: discord.Interaction,
        role: discord.Role
    ) -> None:
        """Displays all granted permissions for the specified role."""
        embed = build_permissions_embed(role)
        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    """Extension setup entry point."""
    await bot.add_cog(Permission(bot))
