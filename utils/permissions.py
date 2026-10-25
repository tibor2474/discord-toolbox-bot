"""Helpers for displaying Discord guild permissions."""

import discord

from config import BOT_COLOR


_CRITICAL_PERMISSIONS = {
    "manage_guild": "Manage Server",
    "ban_members": "Ban Members",
    "kick_members": "Kick Members",
    "manage_channels": "Manage Channels",
}

_PERMISSION_LABELS = {
    "create_instant_invite": "Create Invite",
    "manage_guild": "Manage Server",
    "view_audit_log": "View Audit Log",
    "view_guild_insights": "View Server Insights",
    "manage_emojis": "Manage Emojis",
    "manage_emojis_and_stickers": "Manage Emojis and Stickers",
    "use_external_emojis": "Use External Emojis",
    "use_external_stickers": "Use External Stickers",
    "send_tts_messages": "Send Text-to-Speech Messages",
    "manage_messages": "Manage Messages",
    "read_message_history": "Read Message History",
    "mention_everyone": "Mention Everyone",
    "use_application_commands": "Use Application Commands",
    "manage_webhooks": "Manage Webhooks",
    "manage_roles": "Manage Roles",
    "manage_nicknames": "Manage Nicknames",
    "change_nickname": "Change Nickname",
    "move_members": "Move Members",
    "mute_members": "Mute Members",
    "deafen_members": "Deafen Members",
    "moderate_members": "Timeout Members",
    "use_voice_activation": "Use Voice Activity",
    "priority_speaker": "Priority Speaker",
    "stream": "Video",
    "connect": "Connect to Voice",
    "speak": "Speak in Voice",
    "send_messages": "Send Messages",
    "send_messages_in_threads": "Send Messages in Threads",
    "create_public_threads": "Create Public Threads",
    "create_private_threads": "Create Private Threads",
    "manage_threads": "Manage Threads",
    "view_channel": "View Channels",
    "read_messages": "View Channels",
    "use_external_sounds": "Use External Sounds",
    "send_voice_messages": "Send Voice Messages",
    "send_polls": "Create Polls",
    "use_soundboard": "Use Soundboard",
    "use_external_apps": "Use External Apps",
}


def _permission_label(name: str) -> str:
    """Turn a discord.py permission flag into a readable label."""
    if name in _PERMISSION_LABELS:
        return _PERMISSION_LABELS[name]
    return name.replace("_", " ").capitalize()


def build_permissions_embed(
    subject: discord.Role | discord.Member,
    *,
    title: str | None = None,
) -> discord.Embed:
    """Build an embed listing granted guild permissions for a role or member."""
    permissions = subject.permissions if isinstance(subject, discord.Role) else subject.guild_permissions
    embed = discord.Embed(
        title=title or f"Permissions for {subject.name}",
        color=BOT_COLOR,
    )

    if permissions.administrator:
        embed.add_field(name="Full access", value="- **Administrator**", inline=False)
        return embed

    granted = [name for name, enabled in permissions if enabled and name != "administrator"]
    critical = [name for name in _CRITICAL_PERMISSIONS if name in granted]
    other = [name for name in granted if name not in _CRITICAL_PERMISSIONS]

    if critical:
        embed.add_field(
            name="Critical permissions",
            value="\n".join(f"- **{_CRITICAL_PERMISSIONS[name]}**" for name in critical),
            inline=False,
        )
    if other:
        embed.add_field(
            name="Other permissions",
            value="\n".join(f"- {_permission_label(name)}" for name in other),
            inline=False,
        )
    if not granted:
        embed.description = "No permissions granted."

    return embed
