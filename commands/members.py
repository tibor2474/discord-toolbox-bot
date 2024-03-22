from typing import Union
import discord
from discord.ext import commands

from config import bot_color
from config import image_icon
from config import member_icon


class members(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    
    @discord.slash_command(name="avatar", description="Show someones avatar")
    @discord.option("member", discord.Member, description="Select a user", required=True)
    async def member_avatar(self, ctx, member: discord.Member):
        png = member.avatar.with_format("png")
        jpg = member.avatar.with_format("jpg")
        webp = member.avatar.with_format("webp")

        try:
            gif = member.avatar.with_format("gif")
        except:
            gif = None

        embed = discord.Embed(
            description=f"[PNG]({png}) " f"[JPG]({jpg}) " f"[WEBP]({webp})" f" [GIF]({gif})"
            if gif
            else f"[PNG]({png}) -" f" [JPG]({jpg}) -" f" [WEBP]({webp})",
            color=bot_color)

        embed.set_author(name=f"{member.display_name}'s avatar", icon_url=image_icon)
        embed.set_image(url=member.avatar)
        await ctx.respond(embed=embed)


    @discord.slash_command(name="serveravatar", description="Show someones server avatar", guild_only=True)
    async def member_guild_avatar(self, ctx, member: discord.Member):
        if member.guild_avatar != None:
            png = member.guild_avatar.with_format("png")
            jpg = member.guild_avatar.with_format("jpg")
            webp = member.guild_avatar.with_format("webp")

            try:
                gif = member.guild_avatar.with_format("gif")
            except:
                gif = None

            embed = discord.Embed(
                description=f"[PNG]({png}) " f"[JPG]({jpg}) " f"[WEBP]({webp})" f" [GIF]({gif})"
                if gif
                else f"[PNG]({png}) -" f" [JPG]({jpg}) -" f" [WEBP]({webp})",
                color=bot_color)

            embed.set_author(name=f"{member.display_name}'s server avatar", icon_url=image_icon)
            embed.set_image(url=member.guild_avatar)
            await ctx.respond(embed=embed)
        
        else:
            await ctx.respond(f"{member.display_name} doesn't have a server avatar", ephemeral=True)


    @discord.slash_command(name="banner", description="Show someones banner (if they have one)")
    @discord.option("member", discord.Member, description="Select a user", required=True)
    async def member_banner(self, ctx, member: discord.Member):
        embed = discord.Embed(color=bot_color)

        if member.banner != None:
            embed.set_author(name=f"{member.name}'s banner", icon_url=member_icon)
            embed.set_image(url=member.banner)
            await ctx.respond(embed=embed)
        else:
            await ctx.respond(f"{member.name} doesn't have a banner", ephemeral=True)


    @discord.slash_command(name="vcmove", description="Move member to a different voice channel", guild_only=True)
    @discord.commands.default_permissions(move_members=True)
    @discord.option("member", discord.Member, description="Select a member", required=True)
    @discord.option("channel", Union[discord.VoiceChannel, discord.StageChannel], description="Select a channel", required=True)
    async def member_move(self, ctx, member: discord.Member, channel: Union[discord.VoiceChannel, discord.StageChannel]):
        if member.voice is None:
            await ctx.respond(f"{member.mention} is not in a voice channel", ephemeral=True)
        else:
            await member.move_to(channel, reason=f"command executed by @{ctx.author.name}")
            await ctx.respond(f"Moved {member.mention} to {channel.mention}", ephemeral=True)



def setup(bot: commands.Bot):
    bot.add_cog(members(bot))
    