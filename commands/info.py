import discord
from discord.ext import commands
from config import bot_color, member_icon

class info(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    info = discord.SlashCommandGroup("info", hidden=False)
    
    @info.command()
    async def member(self, ctx: commands.Context, member: discord.Member) -> None:
        creation_time = int(member.created_at.timestamp())
        join_time = int(member.joined_at.timestamp())
    
        embed = discord.Embed(color=bot_color)
        embed.set_thumbnail(url=member.avatar)
        embed.set_author(name="Member info", icon_url=member_icon)
        embed.add_field(name="User name", value=member.name, inline=True)
        embed.add_field(name="Display name", value=member.display_name, inline=True) # since py-cord isn't updated yet, it still shows the member name instead
        embed.add_field(name="Nickname", value=member.nick, inline=True)
            
        embed.add_field(name="Server booster", value=bool(member.premium_since), inline=True)
        embed.add_field(name="In voice", value=bool(member.voice), inline=True)
        embed.add_field(name="Timed out", value=bool(member.timed_out), inline=True)
        
        if member.activity != None:
            embed.add_field(name="Activity", value=member.activity, inline=False)
        else:
            embed.add_field(name="Activity", value="None or hidden", inline=False)

        embed.add_field(name="Bot", value=member.bot, inline=True)
        embed.add_field(name="Status", value=member.status, inline=True)
        embed.add_field(name="User ID", value=f"||{member.id}||", inline=True)
        
        embed.add_field(name="Account created", value=f"<t:{creation_time}:R>", inline=True)
        embed.add_field(name="Joined server", value=f"<t:{join_time}:R>", inline=True)
        await ctx.respond(embed=embed)
    

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
      bot.add_cog(info(bot))