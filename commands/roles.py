import discord
from discord.ext import commands
from config import bot_color, role_icon

class roles(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    
    role = discord.SlashCommandGroup("role", hidden=False)
    
    @role.command(name="show_permissions", description="Show permissions for a role")
    @discord.option("role", discord.Role, description="Select a role", required=True)
    async def role_perms(self, ctx: commands.Context, role: discord.Role) -> None:
        permissions = ', '.join([str(perm[0]).replace("_", " ") for perm in role.permissions if perm[1]])

        if permissions == "":
            permissions = "*There are no permission offsets for this role*"

        embed = discord.Embed(color=bot_color, description=permissions)
        embed.set_author(name=f"Permissions for {role.name}", icon_url=role_icon)
        await ctx.respond(embed=embed)




def setup(bot: commands.Bot) -> None:
    bot.add_cog(roles(bot))