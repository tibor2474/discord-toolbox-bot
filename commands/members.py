import discord
from discord.ext import commands
from config import bot_color, image_icon

class members(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    member = discord.SlashCommandGroup("member", hidden=False)
    
    @member.command()
    @discord.option("member", discord.Member, description="Select a user", required=True)
    async def avatar(self, ctx: commands.Context, member: discord.Member) -> None:
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


    @member.command()
    async def guild_avatar(self, ctx: commands.Context, member: discord.Member) -> None:
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

            embed.set_author(name=f"{member.display_name}'s avatar", icon_url=image_icon)
            embed.set_image(url=member.guild_avatar)
            await ctx.respond(embed=embed)
        
        else:
            embed = discord.Embed(color=bot_color)
            embed.set_author(name=f"{member.display_name} doesn't have a guild avatar", icon_url=image_icon)
            await ctx.respond(embed=embed)


    @member.command()
    @discord.option("member", discord.Member, description="Select a user", required=True)
    async def banner(self, ctx: commands.Context, member: discord.Member) -> None:
        embed = discord.Embed(color=bot_color)

        if member.banner != None:
            embed.set_author(name=f"{member.name}'s banner", icon_url=member_icon)
            embed.set_image(url=member.banner)
        else:
            embed.set_author(name=f"{member.name} doesn't have a banner", icon_url=image_icon)

        await ctx.respond(embed=embed)



def setup(bot: commands.Bot) -> None:
    bot.add_cog(members(bot))