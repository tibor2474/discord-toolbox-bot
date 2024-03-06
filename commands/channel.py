import discord
from discord.ext import commands
from typing import Union

class channel(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    @discord.slash_command(name="slowmode", description="Set custom slowmode for a channel", guild_only=True)
    @discord.commands.default_permissions(manage_channels=True)
    @discord.option("channel", Union[discord.TextChannel, discord.StageChannel, discord.VoiceChannel], description="Select a channel", required=True)
    @discord.option("seconds", int, description="Slowmode delay in seconds (set to 0 to disable)", required=True)
    async def channel_slowmode(self, ctx, channel: Union[discord.TextChannel, discord.StageChannel, discord.VoiceChannel], seconds: int):
        await channel.edit(slowmode_delay=seconds)
        if seconds == 0:
            return await ctx.respond(f"Disabled slowmode for {channel.mention}")
        await ctx.respond(f"Changed slowmode for {channel.mention} to {seconds} seconds")


    @discord.slash_command(name="nsfw", description="Turn on or off age-restricted mode for a channel", guild_only=True)
    @discord.commands.default_permissions(manage_channels=True)
    @discord.option("channel", Union[discord.TextChannel, discord.StageChannel, discord.VoiceChannel, discord.ForumChannel], description="Select a channel", required=True)
    @discord.option("mode", bool, description="Turn on or off", required=True)
    async def channel_nsfw(self, ctx, channel: Union[discord.TextChannel, discord.StageChannel, discord.VoiceChannel, discord.ForumChannel], mode: bool):
        if mode == True:
            await channel.edit(nsfw=True)
            await ctx.respond(f"Turned on age-restriction for {channel.mention}")
        elif mode == False:
            await channel.edit(nsfw=False)
            await ctx.respond(f"Turned off age-restriction for {channel.mention}")

    
    @discord.slash_command(name="vclimit", description="Set user limit for voice channels", guild_only=True)
    @discord.commands.default_permissions(manage_channels=True)
    @discord.option("channel", Union[discord.StageChannel, discord.VoiceChannel], description="Select a channel", required=True)
    @discord.option("limit", int, description="User limit (set to 0 to disable)", required=True)
    async def channel_limit(self, ctx, channel: Union[discord.StageChannel, discord.VoiceChannel], limit: int):
        await channel.edit(user_limit=limit)
        if limit == 0:
            return await ctx.respond(f"Disabled user limit for {channel.mention}")
        await ctx.respond(f"Changed user limit for {channel.mention} to {limit} members")


    @discord.slash_command(name="vcregion", description="Change region for a voice channel", guild_only=True)
    @discord.commands.default_permissions(manage_channels=True)
    @discord.option("channel", Union[discord.StageChannel, discord.VoiceChannel], description="Select a channel", required=True)
    @discord.option("region", str, description="Select a region", required=True, choices=[
        "Automatic",
        "Brazil",
        "Hong Kong",
        "India",
        "Japan",
        "Rotterdam",
        "Russia",
        "Singapore",
        "South Africa",
        "Sydney",
        "US Central",
        "US East",
        "US South",
        "US West"
    ])
    async def channel_region(self, ctx, channel: Union[discord.StageChannel, discord.VoiceChannel], region: str) -> None:
        global set_region
        if region == "Automatic":
            set_region = None
        elif region == "Hong Kong":
            set_region = "hongkong"
        elif region == "South Africa":
            set_region = "southafrica"
        else:
            set_region = region.lower().replace(" ", "_")

        try:
            await channel.edit(rtc_region=set_region, reason=f"command executed by @{ctx.author.name}")
            await ctx.respond(f"Changed region to {region} for {channel.mention}", ephemeral=True)
        except:
            await ctx.respond(f"Failed to change region for {channel.mention}")



def setup(bot: commands.Bot) -> None:
      bot.add_cog(channel(bot))