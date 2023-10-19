import discord
from discord.ext import commands
from typing import Union
from config import bot_color, image_icon, member_icon

class members(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    member = discord.SlashCommandGroup("member", "Commands for member things", hidden=False, guild_only=True, default_member_permissions=discord.Permissions(kick_members=True, move_members=True))
    
    @member.command(name="avatar", description="Show someones avatar")
    @discord.option("member", discord.Member, description="Select a user", required=True)
    async def member_avatar(self, ctx: commands.Context, member: discord.Member) -> None:
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


    @member.command(name="guild_avatar", description="Show someones server avatar")
    async def member_guild_avatar(self, ctx: commands.Context, member: discord.Member) -> None:
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
            await ctx.respond(f"{member.display_name} doesn't have a server avatar")


    @member.command(name="banner", description="Show someones banner (if they have one)")
    @discord.option("member", discord.Member, description="Select a user", required=True)
    async def member_banner(self, ctx: commands.Context, member: discord.Member) -> None:
        embed = discord.Embed(color=bot_color)

        if member.banner != None:
            embed.set_author(name=f"{member.name}'s banner", icon_url=member_icon)
            embed.set_image(url=member.banner)
            await ctx.respond(embed=embed)
        else:
            await ctx.respond(f"{member.name} doesn't have a banner")


    @member.command(name="move", description="Move member to a different voice channel")
    @discord.option("member", discord.Member, description="Select a member", required=True)
    @discord.option("channel", Union[discord.VoiceChannel, discord.StageChannel], description="Select a channel", required=True)
    async def member_move(self, ctx: commands.Context, member: discord.Member, channel: Union[discord.VoiceChannel, discord.StageChannel]) -> None:
        if member.voice is None:
            await ctx.respond(f"{member.mention} is not in a voice channel", ephemeral=True)
        else:
            await member.move_to(channel, reason=f"command executed by @{ctx.author.name}")
            await ctx.respond(f"Moved {member.mention} to {channel.mention}", ephemeral=True)



def setup(bot: commands.Bot) -> None:
    bot.add_cog(members(bot))