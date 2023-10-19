import discord
from discord.ext import commands
from config import bot_color, member_icon, server_icon, role_icon

class info(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    info = discord.SlashCommandGroup("info", "Get info", hidden=False, default_member_permissions=discord.Permissions(kick_members=True, manage_roles=True))
    
    @info.command(name="member", description="Show info about someone")
    @discord.option("member", discord.Member, description="Select someone", required=True)
    async def info_member(self, ctx: commands.Context, member: discord.Member) -> None:
        creation_time = int(member.created_at.timestamp())
        join_time = int(member.joined_at.timestamp())
    
        embed = discord.Embed(color=bot_color)
        embed.set_thumbnail(url=member.avatar)
        embed.set_author(name="Member info", icon_url=member_icon)
        embed.add_field(name="User name", value=member.name, inline=True)
        embed.add_field(name="Display name", value=member.display_name, inline=True) # since py-cord isn't updated yet, it still shows the member name instead
        embed.add_field(name="Nickname", value=member.nick, inline=True)
            
        embed.add_field(name="Server booster", value=bool(member.premium_since), inline=True)
        embed.add_field(name="In voice", value=bool(member.voice), inline=True)
        embed.add_field(name="Timed out", value=bool(member.timed_out), inline=True)
        
        if member.activity != None:
            embed.add_field(name="Activity", value=member.activity, inline=False)
        else:
            embed.add_field(name="Activity", value="*None/hidden or offline*", inline=False)

        embed.add_field(name="Bot", value=member.bot, inline=True)
        embed.add_field(name="Status", value=member.status, inline=True)
        embed.add_field(name="User ID", value=f"||{member.id}||", inline=True)
        
        embed.add_field(name="Account created", value=f"<t:{creation_time}:R>", inline=True)
        embed.add_field(name="Joined server", value=f"<t:{join_time}:R>", inline=True)
        await ctx.respond(embed=embed)
    

    @info.command(name="server", description="Show info about this server")
    async def info_server(self, ctx: commands.Context) -> None:
        guild = ctx.guild
        user_count = len([m for m in guild.members if not m.bot])
        bot_count = len([b for b in guild.members if b.bot])
        category_count = len(guild.categories)
        text_count = len(guild.text_channels)
        voice_count = len(guild.voice_channels)
        forum_count = len(guild.forum_channels)
        stage_count = len(guild.stage_channels)
        guild_date = int(guild.created_at.timestamp())
        file_limit = guild.filesize_limit / 1048576 # covert byte to megabyte
        afk_timeout = guild.afk_timeout / 60

        if guild.mfa_level == 0:
            mfa_level = "None"
        elif guild.mfa_level == 1:
            mfa_level = "Low"
        elif guild.mfa_level == 2:
            mfa_level = "Medium"
        elif guild.mfa_level == 3:
            mfa_level = "High"
        elif guild.mfa_level == 4:
            mfa_level = "Very High"

        if guild.afk_channel == None:
            afk_channel = "Not set"
        else:
            afk_channel = guild.afk_channel.mention

        if guild.description != None:
            embed = discord.Embed(description="**Server description**\n" + guild.description, color=bot_color)
        else:
            embed = discord.Embed(color=bot_color)
        
        embed.set_author(name="Server info", icon_url=server_icon)
        embed.add_field(name="Name", value=f"{guild.name}", inline=False)

        embed.add_field(name="Owner", value=f"@{guild.owner.name}", inline=True) # guild.owner shows username#0 so used guild.owner.name as a workaround
        embed.add_field(name="Region", value=f"{guild.preferred_locale}", inline=True)
        embed.add_field(name="Verification level", value=f"{mfa_level}", inline=True)

        embed.add_field(name="Server boosts", value=f"{guild.premium_subscription_count} boosts\n{len(guild.premium_subscribers)} booster", inline=True)
        embed.add_field(name="AFK channel", value=f"{afk_channel}\n{afk_timeout} min timeout", inline=True)
        embed.add_field(name="Emojis and stickers", value=f"{len(guild.emojis)} emojis\n{len(guild.stickers)} stickers")
        
        embed.add_field(name="Channels", value=f"{category_count} categories\n{text_count} text\n{voice_count} voice\n{forum_count} forum\n{stage_count} stage", inline=True)
        embed.add_field(name="Limits", value=f"{file_limit} MB files\n{guild.sticker_limit} stickers\n{guild.emoji_limit} emojis\n{guild.max_members} users", inline=True)
        embed.add_field(name="Members", value=f"{user_count} users\n{bot_count} bots", inline=True)

        embed.add_field(name="Roles", value=f"{len(guild.roles)} roles", inline=True)
        embed.add_field(name="Created", value=f"<t:{guild_date}:R>", inline=True)
        
        embed.add_field(name="Server ID", value=f"||{guild.id}||", inline=False)
        
        if guild.icon != None:
            embed.set_thumbnail(url=guild.icon)

        await ctx.respond(embed=embed)


    @info.command(name="role", description="Show info about a role")
    @discord.option("role", discord.Role, description="Select a role", required=True)
    async def info_role(self, ctx: commands.Context, role: discord.Role):
        creation_time = int(role.created_at.timestamp())

        embed = discord.Embed(color=bot_color)
        embed.set_author(name="Role info", icon_url=role_icon)
        embed.add_field(name="Role name", value=role.name, inline=False)

        if role.icon != None:
            embed.set_thumbnail(url=role.icon)
        elif role.unicode_emoji != None:
            embed.add_field(name="Emoji", value=role.unicode_emoji, inline=True)
            
        embed.add_field(name="Color", value=role.color, inline=True)
        embed.add_field(name="Mentionable", value=role.mentionable, inline=True)
        embed.add_field(name="Managed by integration", value=role.managed, inline=True)
        
        embed.add_field(name="Assigned to", value=f'{len(role.members)} members', inline=True)
        embed.add_field(name="Position", value=role.position, inline=True)

        embed.add_field(name="Displayed separately", value=role.hoist, inline=True)
        embed.add_field(name="Created", value=f"<t:{creation_time}:R>", inline=True)
        embed.add_field(name="Role ID", value=f"||{role.id}||", inline=True)

        await ctx.respond(embed=embed)



def setup(bot: commands.Bot) -> None:
      bot.add_cog(info(bot))