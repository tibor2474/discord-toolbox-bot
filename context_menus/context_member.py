import discord
from discord.ext import commands

from config import bot_color
from config import member_icon


class context_member(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @discord.user_command(name="Show info")
    @discord.commands.default_permissions(kick_members=True)
    async def info_member(self, ctx, member: discord.Member):
        creation_time = int(member.created_at.timestamp())
        join_time = int(member.joined_at.timestamp())
    
        embed = discord.Embed(color=bot_color)
        embed.set_thumbnail(url=member.avatar)
        embed.set_author(name="Member info", icon_url=member_icon)
        embed.add_field(name="User mention", value=member.mention, inline=True)
        embed.add_field(name="User name", value=member.name, inline=True)
        embed.add_field(name="Nickname", value=member.nick, inline=True)
            
        embed.add_field(name="Server booster", value=bool(member.premium_since), inline=True)
        embed.add_field(name="In voice", value=bool(member.voice), inline=True)
        embed.add_field(name="Timed out", value=bool(member.timed_out), inline=True)
        
        if member.activity != None:
            embed.add_field(name="Activity", value=member.activity, inline=False)
        else:
            embed.add_field(name="Activity", value="*None/hidden or offline*", inline=False)

        embed.add_field(name="Bot", value=member.bot, inline=True)
        embed.add_field(name="Status", value=member.status, inline=True)
        embed.add_field(name="User ID", value=f"||{member.id}||", inline=True)
        
        embed.add_field(name="Account created", value=f"<t:{creation_time}:R>", inline=True)
        embed.add_field(name="Joined server", value=f"<t:{join_time}:R>", inline=True)
        await ctx.respond(embed=embed, ephemeral=True)



def setup(bot: commands.Bot):
    bot.add_cog(context_member(bot))
      