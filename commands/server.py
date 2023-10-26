import discord
from discord.ext import commands
from config import bot_color, image_icon, emoji_icon

class server(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    server = discord.SlashCommandGroup("server", "Server managemnt", hidden=False, guild_only=True, default_member_permissions=discord.Permissions(kick_members=True, manage_roles=True))

    @server.command(name="icon", description="Show server icon")
    async def guild_icon(self, ctx: commands.Context) -> None:
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


    @server.command(name="banner", description="Show server banner image")
    async def guild_banner(self, ctx: commands.Context) -> None:
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


    @server.command(name="invite_background", description="Show server invite background")
    async def guild_invite_background(self, ctx: commands.Context) -> None:
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


    @server.command(name="emojis", description="Show server emojis")
    async def guild_emojis(self, ctx: commands.Context) -> None:
        guild = ctx.guild
        emojis = [str(x) for x in guild.emojis]

        embed = discord.Embed(color=bot_color, description=" ".join(emojis))
        embed.set_author(name="Server emojis", icon_url=emoji_icon)
        embed.set_footer(text=f"{len(emojis)} emojis total")
        await ctx.respond(embed=embed, ephemeral=True)


def setup(bot: commands.Bot) -> None:
      bot.add_cog(server(bot))