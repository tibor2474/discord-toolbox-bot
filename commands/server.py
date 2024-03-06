import discord
from discord.ext import commands
from config import bot_color, image_icon, emoji_icon

class server(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    @discord.slash_command(name="servericon", description="Show server icon", guild_only=True)
    async def guild_icon(self, ctx) -> None:
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
            await ctx.respond(f"This server doesn't have an icon", ephemeral=True)


    @discord.slash_command(name="serverbanner", description="Show server banner image", guild_only=True)
    async def guild_banner(self, ctx) -> None:
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
            await ctx.respond(f"This server doesn't have a banner", ephemeral=True)


    @discord.slash_command(name="serverbackground", description="Show server invite background", guild_only=True)
    async def guild_invite_background(self, ctx) -> None:
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
            await ctx.respond(f"This server doesn't have an invite background", ephemeral=True)


    @discord.slash_command(name="serveremojis", description="Show server emojis", guild_only=True)
    async def guild_emojis(self, ctx) -> None:
        guild = ctx.guild
        emojis = [str(x) for x in guild.emojis]

        embed = discord.Embed(color=bot_color, description=" ".join(emojis))
        embed.set_author(name="Server emojis", icon_url=emoji_icon)
        embed.set_footer(text=f"{len(emojis)} emojis total")
        await ctx.respond(embed=embed, ephemeral=True)


def setup(bot: commands.Bot) -> None:
      bot.add_cog(server(bot))