import discord
from discord.ext import commands
from config import bot_color, role_icon

class roles(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    
    #role = discord.SlashCommandGroup("role", "Role commands", hidden=False, default_member_permissions=discord.Permissions(manage_roles=True))


def setup(bot: commands.Bot) -> None:
    bot.add_cog(roles(bot))