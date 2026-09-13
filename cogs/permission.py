"""Permission inspection commands for members and roles."""

import discord
from discord import app_commands
from discord.ext import commands

from config import bot_color, member_icon, role_icon


@app_commands.default_permissions(manage_roles=True)
@app_commands.guild_only()
class Permission(commands.GroupCog, name="permission", description="Manage and view permissions"):
    """Cog for viewing role and member permissions within the guild."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    @app_commands.command(name="showmember", description="Show permissions for a member")
    @app_commands.describe(member="Select a member")
    async def show_member_perms(
        self,
        interaction: discord.Interaction,
        member: discord.Member
    ) -> None:
        """Displays all granted guild permissions for the specified member."""
        permissions = ", ".join(
            str(perm[0]).replace("_", " ") for perm in member.guild_permissions if perm[1]
        )

        if not permissions:
            permissions = "*There are no permissions for this member*"

        embed = discord.Embed(color=bot_color, description=permissions)
        embed.set_author(name=f"Permissions for {member.name}", icon_url=member_icon)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="showrole", description="Show permissions for a role")
    @app_commands.describe(role="Select a role")
    async def show_role_perms(
        self,
        interaction: discord.Interaction,
        role: discord.Role
    ) -> None:
        """Displays all granted permissions for the specified role."""
        permissions = ", ".join(
            str(perm[0]).replace("_", " ") for perm in role.permissions if perm[1]
        )

        if not permissions:
            permissions = "*There are no permission offsets for this role*"

        embed = discord.Embed(color=bot_color, description=permissions)
        embed.set_author(name=f"Permissions for {role.name}", icon_url=role_icon)
        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    """Extension setup entry point."""
    await bot.add_cog(Permission(bot))
