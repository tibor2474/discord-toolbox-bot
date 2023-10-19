import discord
from discord.ext import commands
from config import bot_color, member_icon, role_icon

class permission(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    permission = discord.SlashCommandGroup("permission", "Modify permissions", hidden=False, default_member_permissions=discord.Permissions(manage_roles=True))
    show = permission.create_subgroup("show", "Show permissions")

    @show.command(name="member", description="Show permissions for a member")
    @discord.option("member", discord.Member, description="Select a member", required=True)
    async def show_member_perms(self, ctx: commands.Context, member: discord.Member) -> None:
        permissions = ', '.join([str(perm[0]).replace("_", " ") for perm in member.guild_permissions if perm[1]])

        if permissions == "":
            permissions = "*There are no permissions for this member*"

        embed = discord.Embed(color=bot_color, description=permissions)
        embed.set_author(name=f"Permissions for {member.name}", icon_url=member_icon)
        await ctx.respond(embed=embed)


    @show.command(name="role", description="Show permissions for a role")
    @discord.option("role", discord.Role, description="Select a role", required=True)
    async def show_role_perms(self, ctx: commands.Context, role: discord.Role) -> None:
        permissions = ', '.join([str(perm[0]).replace("_", " ") for perm in role.permissions if perm[1]])

        if permissions == "":
            permissions = "*There are no permission offsets for this role*"

        embed = discord.Embed(color=bot_color, description=permissions)
        embed.set_author(name=f"Permissions for {role.name}", icon_url=role_icon)
        await ctx.respond(embed=embed)


def setup(bot: commands.Bot) -> None:
      bot.add_cog(permission(bot))