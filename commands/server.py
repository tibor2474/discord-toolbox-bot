import discord
from discord.ext import commands
from config import bot_color, image_icon

class server(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    server = discord.SlashCommandGroup("server", hidden=False)

    @server.command()
    async def icon(self, ctx: commands.Context) -> None:
        guild = ctx.guild
        if guild.icon != None:
            png = guild.icon.with_format("png")
            jpg = guild.icon.with_format("jpg")
            webp = guild.icon.with_format("webp")

            try:
                gif = guild.icon.with_format("gif")
            except:
                gif = None

            embed = discord.Embed(
                description=f"[PNG]({png}) - [JPG]({jpg}) - [WEBP]({webp}) - [GIF]({gif})"
                if gif
                else f"[PNG]({png}) - [JPG]({jpg}) - [WEBP]({webp})",
                color=bot_color)

            embed.set_author(name="Server icon", icon_url=image_icon)
            embed.set_image(url=guild.icon)
            await ctx.respond(embed=embed)
        
        else:
            await ctx.respond(f"This server doesn't have an icon")


    @server.command()
    async def banner(self, ctx: commands.Context) -> None:
        guild = ctx.guild
        if guild.banner != None:
            png = guild.banner.with_format("png")
            jpg = guild.banner.with_format("jpg")
            webp = guild.banner.with_format("webp")
            # no gif because animated banners are not a thing yet

            embed = discord.Embed(
                description=f"[PNG]({png}) -" f"[JPG]({jpg}) -" f"[WEBP]({webp})", 
                color=bot_color)

            embed.set_author(name="Server banner", icon_url=image_icon)
            embed.set_image(url=guild.banner)
            await ctx.respond(embed=embed)

        else:
            await ctx.respond(f"This server doesn't have a banner")


    @server.command()
    async def invite_background(self, ctx: commands.Context) -> None:
        guild = ctx.guild
        if guild.splash != None:
            png = guild.splash.with_format("png")
            jpg = guild.splash.with_format("jpg")
            webp = guild.splash.with_format("webp")

            embed = discord.Embed(
                description=f"[PNG]({png}) -" f"[JPG]({jpg}) -" f"[WEBP]({webp})", 
                color=bot_color)

            embed.set_author(name="Server invite background", icon_url=image_icon)
            embed.set_image(url=guild.splash)
            await ctx.respond(embed=embed)

        else:
            await ctx.respond(f"This server doesn't have an invite background")



def setup(bot: commands.Bot) -> None:
      bot.add_cog(server(bot))