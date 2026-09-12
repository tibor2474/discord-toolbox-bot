import discord
from discord.ext import commands


class thread(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @discord.slash_command(name="threadclose", description="Allows a staff member or the thread owner to close the thread", guild_only=True)
    @discord.option("lock", bool, description="Lock thread?", required=True)
    async def thread_close(self, ctx, lock: bool = False):
        assert isinstance(ctx.author, discord.Member)
        if not isinstance(ctx.channel, discord.Thread):
            return await ctx.respond("This command can only be used in threads.", ephemeral=True)

        if ctx.channel.permissions_for(ctx.author).manage_threads:
            if lock:
                await ctx.respond("This thread was archived and locked by a staff member.")

            else:
                await ctx.respond("This thread was archived by a staff member.")
            await ctx.channel.archive(locked=lock)

        elif ctx.author.id == ctx.channel.owner_id:
            await ctx.respond("This thread was archived by the user that opened it.")
            await ctx.channel.archive()

        else:
            await ctx.respond("This command can only be used by the owner of the thread or a staff member.", ephemeral=True)


    @discord.slash_command(name="threadname", description="Change the name of the thread", guild_only=True)
    @discord.option("name", str, description="New name for this thread", required=True)
    async def thread_name(self, ctx, name: str):
        assert isinstance(ctx.author, discord.Member)
        if not isinstance(ctx.channel, discord.Thread):
            return await ctx.respond("This command can only be used in threads.", ephemeral=True)

        if ctx.channel.permissions_for(ctx.author).manage_threads or ctx.author.id == ctx.channel.owner_id:
            await ctx.channel.edit(name=name)
            await ctx.respond(f"Changed thread name to: **{name}**")

        else:
            await ctx.respond("This command can only be used by the owner of the thread or a staff member.", ephemeral=True)


    @discord.slash_command(name="threadslowmode", description="Set custom slowmode for a thread", guild_only=True)
    @discord.commands.default_permissions(manage_channels=True)
    @discord.option("seconds", int, description="Slowmode delay in seconds (set to 0 to disable)", required=True)
    async def thread_slowmode(self, ctx, seconds: int):
        assert isinstance(ctx.author, discord.Member)
        if not isinstance(ctx.channel, discord.Thread):
            return await ctx.respond("This command can only be used in threads.", ephemeral=True)

        channel = ctx.channel
        await channel.edit(slowmode_delay=seconds)

        if seconds == 0:
            return await ctx.respond("Disabled slowmode")
        await ctx.respond(f"Changed slowmode to {seconds} seconds")


def setup(bot: commands.Bot):
    bot.add_cog(thread(bot))
      