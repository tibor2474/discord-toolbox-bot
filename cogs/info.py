"""Informational commands for server, roles, and bot statistics."""

import discord
from discord import app_commands
from discord.ext import commands

from config import BOT_COLOR


class Info(commands.Cog):
    """Cog for displaying detailed information about members, servers, and roles."""

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="memberinfo", description="Show info about someone")
    @app_commands.guild_only()
    @app_commands.default_permissions(kick_members=True)
    @app_commands.describe(member="Select someone")
    async def info_member(self, interaction: discord.Interaction, member: discord.Member) -> None:
        """Displays information about a server member."""
        if member.discriminator and member.discriminator != "0":
            membername = f"{member.name}#{member.discriminator}"
        else:
            membername = member.name

        creation_time = int(member.created_at.timestamp())
        join_time = int(member.joined_at.timestamp()) if member.joined_at else 0

        embed = discord.Embed(color=BOT_COLOR, title="Member info")
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="User mention", value=member.mention, inline=True)
        embed.add_field(name="Display name", value=member.display_name, inline=True)
        embed.add_field(name="Nickname", value=member.nick or "*None*", inline=True)
        embed.add_field(name="Username", value=membername, inline=True)

        embed.add_field(name="Server booster", value=bool(member.premium_since), inline=True)
        embed.add_field(name="In voice", value=bool(member.voice), inline=True)
        embed.add_field(name="Timed out", value=member.is_timed_out(), inline=True)

        if member.activity is not None:
            embed.add_field(name="Activity", value=str(member.activity), inline=True)
        else:
            embed.add_field(name="Activity", value="*None/hidden or offline*", inline=True)

        embed.add_field(name="Bot", value=member.bot, inline=True)
        embed.add_field(name="Status", value=str(member.status), inline=True)
        embed.add_field(name="User ID", value=f"||{member.id}||", inline=True)

        embed.add_field(name="Account created", value=f"<t:{creation_time}:R>", inline=True)
        embed.add_field(name="Joined server", value=f"<t:{join_time}:R>", inline=True)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="serverinfo", description="Show info about this server")
    @app_commands.guild_only()
    @app_commands.default_permissions(manage_guild=True)
    async def info_server(self, interaction: discord.Interaction) -> None:
        """Displays detailed statistics and configuration for the current server."""
        guild = interaction.guild
        if guild is None:
            await interaction.response.send_message(
                "This command can only be used in a server.",
                ephemeral=True
            )
            return

        cached_user_count = len([member for member in guild.members if not member.bot])
        cached_bot_count = len([member for member in guild.members if member.bot])
        category_count = len(guild.categories)
        text_count = len(guild.text_channels)
        voice_count = len(guild.voice_channels)
        forum_count = sum(
            isinstance(channel, discord.ForumChannel)
            for channel in guild.channels
        )
        stage_count = len(guild.stage_channels)
        guild_date = int(guild.created_at.timestamp())
        file_limit = guild.filesize_limit / 1048576  # convert bytes to megabytes
        afk_timeout = int(guild.afk_timeout / 60)

        mfa_level = "enabled" if guild.mfa_level == discord.MFALevel.require_2fa else "disabled"
        afk_channel = guild.afk_channel.mention if guild.afk_channel else "Not set"

        if guild.description:
            embed = discord.Embed(
                description=f"**Server description**\n{guild.description}",
                title="Server info",
                color=BOT_COLOR
            )
        else:
            embed = discord.Embed(color=BOT_COLOR, title="Server info")

        embed.add_field(name="Name", value=f"{guild.name}", inline=False)

        owner_mention = guild.owner.mention if guild.owner else "Unknown"
        embed.add_field(name="Owner", value=owner_mention, inline=True)
        embed.add_field(name="Region", value=f"{guild.preferred_locale}", inline=True)
        embed.add_field(
            name="Verification level",
            value=f"{guild.verification_level} (2fa {mfa_level})",
            inline=True
        )

        embed.add_field(
            name="Server boosts",
            value=(
                f"{guild.premium_subscription_count} boosts\n"
                f"{len(guild.premium_subscribers)} booster"
            ),
            inline=True
        )
        embed.add_field(
            name="AFK channel",
            value=f"{afk_channel}\n{afk_timeout} min timeout",
            inline=True
        )
        embed.add_field(
            name="Emojis and stickers",
            value=f"{len(guild.emojis)} emojis\n{len(guild.stickers)} stickers",
            inline=True
        )

        channels_desc = (
            f"{category_count} categories\n{text_count} text\n"
            f"{voice_count} voice\n{forum_count} forum\n{stage_count} stage"
        )
        embed.add_field(name="Channels", value=channels_desc, inline=True)

        limits_desc = (
            f"{file_limit:.1f} MB files\n{guild.sticker_limit} stickers\n"
            f"{guild.emoji_limit} emojis\n{guild.max_members} users"
        )
        embed.add_field(name="Limits", value=limits_desc, inline=True)
        embed.add_field(
            name="Members",
            value=(
                f"{guild.member_count} total\n"
                f"{cached_user_count} users, {cached_bot_count} bots"
            ),
            inline=True
        )

        embed.add_field(name="Roles", value=f"{len(guild.roles)} roles", inline=True)
        embed.add_field(name="Created", value=f"<t:{guild_date}:R>", inline=True)
        embed.add_field(name="Server ID", value=f"||{guild.id}||", inline=True)

        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="roleinfo", description="Show info about a role")
    @app_commands.guild_only()
    @app_commands.default_permissions(manage_roles=True)
    @app_commands.describe(role="Select a role")
    async def info_role(self, interaction: discord.Interaction, role: discord.Role) -> None:
        """Displays attributes and permissions for the specified role."""
        creation_time = int(role.created_at.timestamp())

        embed = discord.Embed(color=BOT_COLOR, title="Role info")
        embed.add_field(name="Role name", value=role.name, inline=False)

        if role.icon:
            embed.set_thumbnail(url=role.icon.url)
        elif role.unicode_emoji:
            embed.add_field(name="Emoji", value=role.unicode_emoji, inline=True)

        embed.add_field(name="Color", value=str(role.color), inline=True)
        embed.add_field(name="Mentionable", value=str(role.mentionable), inline=True)
        embed.add_field(name="Managed by integration", value=str(role.managed), inline=True)

        embed.add_field(name="Assigned to", value=f"{len(role.members)} members", inline=True)
        embed.add_field(name="Position", value=str(role.position), inline=True)

        embed.add_field(name="Displayed separately", value=str(role.hoist), inline=True)
        embed.add_field(name="Created", value=f"<t:{creation_time}:R>", inline=True)
        embed.add_field(name="Role ID", value=f"||{role.id}||", inline=True)

        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    """Extension setup entry point."""
    await bot.add_cog(Info(bot))
