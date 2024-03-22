import discord
from discord.ext import commands

from config import bot_color
from config import message_icon


class context_message(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @discord.message_command(name="Show raw message")
    async def raw_message(self, ctx, message: discord.Message):
        if message.content == "":
            return await ctx.respond("The message doesn't have any content that i can show", ephemeral=True)   

        embed = discord.Embed(color=bot_color, title=f"Raw of ID:{message.id}", description=f"```{message.content}```")
        embed.set_author(name="Raw message", icon_url=message_icon)
        embed.set_footer(text="The formating might be inaccurate if you're viewing code blocks")
        await ctx.respond(embed=embed, ephemeral=True) 



def setup(bot: commands.Bot):
    bot.add_cog(context_message(bot))
