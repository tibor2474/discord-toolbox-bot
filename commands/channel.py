import discord
from discord.ext import commands
from typing import Union
from config import bot_color

class channel(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    channel = discord.SlashCommandGroup("channel", hidden=False)

    @channel.command(name="slowmode", description="Set custom slowmode for a channel")
    @discord.option("channel", Union[discord.TextChannel, discord.StageChannel, discord.VoiceChannel], description="Select a channel", required=True)
    @discord.option("seconds", int, description="Slowmode delay in seconds (set to 0 to disable)", required=True)
    async def channel_slowmode(self, ctx: commands.Context, channel: Union[discord.TextChannel, discord.StageChannel, discord.VoiceChannel], seconds: int):
        await channel.edit(slowmode_delay=seconds)
        if seconds == 0:
            return await ctx.respond(f"Disabled slowmode for {channel.mention}")
        await ctx.respond(f"Changed slowmode for {channel.mention} to {seconds} seconds")


    @channel.command(name="nsfw", description="Turn on or off age-restricted mode")
    @discord.option("channel", Union[discord.TextChannel, discord.StageChannel, discord.VoiceChannel, discord.ForumChannel], description="Select a channel", required=True)
    @discord.option("mode", bool, description="Turn on or off", required=True)
    async def channel_nsfw(self, ctx: commands.Context, channel: Union[discord.TextChannel, discord.StageChannel, discord.VoiceChannel, discord.ForumChannel], mode: bool):
        if mode == True:
            await channel.edit(nsfw=True)
            await ctx.respond(f"Turned on age-restriction for {channel.mention}")
        elif mode == False:
            await channel.edit(nsfw=False)
            await ctx.respond(f"Turned off age-restriction for {channel.mention}")

    
    @channel.command(name="limit", description="Set user limit for voice channels")
    @discord.option("channel", Union[discord.StageChannel, discord.VoiceChannel], description="Select a channel", required=True)
    @discord.option("limit", int, description="User limit (set to 0 to disable)", required=True)
    async def channel_limit(self, ctx: commands.Context, channel: Union[discord.StageChannel, discord.VoiceChannel], limit: int):
        await channel.edit(user_limit=limit)
        if limit == 0:
            return await ctx.respond(f"Disabled user limit for {channel.mention}")
        await ctx.respond(f"Changed user limit for {channel.mention} to {limit} members")



def setup(bot: commands.Bot) -> None:
      bot.add_cog(channel(bot))