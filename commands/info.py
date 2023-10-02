import discord
from discord.ext import commands
from config import bot_color

class members(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    info = discord.SlashCommandGroup("info", hidden=False)
    
    @info.command()
    async def member(self, ctx):
      await ctx.respond(f"member")
    
    @info.command()
    async def server(self, ctx):
      await ctx.respond(f"server")

    @info.command()
    async def channel(self, ctx):
      await ctx.respond(f"channel")

    @info.command()
    async def role(self, ctx):
      await ctx.respond(f"role")



def setup(bot: commands.Bot) -> None:
    bot.add_cog(members(bot))