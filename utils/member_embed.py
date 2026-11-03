"""Shared member information embed builders."""

import discord

from config import BOT_COLOR


def build_member_embed(member: discord.Member) -> discord.Embed:
    """Build the embed used by member information commands."""
    if member.discriminator and member.discriminator != "0":
        username = f"{member.name}#{member.discriminator}"
    else:
        username = member.name

    creation_time = int(member.created_at.timestamp())
    join_time = int(member.joined_at.timestamp()) if member.joined_at else 0

    embed = discord.Embed(color=BOT_COLOR, title="Member info")
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.add_field(name="User mention", value=member.mention, inline=True)
    embed.add_field(name="Display name", value=member.display_name, inline=True)
    embed.add_field(name="Nickname", value=member.nick or "*None*", inline=True)
    embed.add_field(name="Username", value=username, inline=True)

    embed.add_field(name="Server booster", value=bool(member.premium_since), inline=True)
    embed.add_field(name="In voice", value=bool(member.voice), inline=True)
    embed.add_field(name="Timed out", value=member.is_timed_out(), inline=True)

    activity = str(member.activity) if member.activity is not None else "*None/hidden or offline*"
    embed.add_field(name="Activity", value=activity, inline=True)

    embed.add_field(name="Bot", value=member.bot, inline=True)
    embed.add_field(name="Status", value=str(member.status), inline=True)
    embed.add_field(name="User ID", value=f"||{member.id}||", inline=True)

    embed.add_field(name="Account created", value=f"<t:{creation_time}:R>", inline=True)
    embed.add_field(name="Joined server", value=f"<t:{join_time}:R>", inline=True)
    return embed
