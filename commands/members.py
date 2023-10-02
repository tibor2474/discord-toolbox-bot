import discord
from discord.ext import commands
from config import bot_color, image_icon

class members(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    member = discord.SlashCommandGroup("member", hidden=False)
    
    @member.command()
    async def avatar(self, ctx):
      await ctx.respond(f"avatar")
    
    @member.command()
    async def guild_avatar(self, ctx):
      await ctx.respond(f"guild_avatar")

    @member.command()
    async def banner(self, ctx):
      await ctx.respond(f"banner")



def setup(bot: commands.Bot) -> None:
    bot.add_cog(members(bot))