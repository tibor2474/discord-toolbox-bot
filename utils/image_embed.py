"""Shared image asset embed builders."""

import discord


def build_image_embed(
    asset: discord.Asset,
    *,
    title: str,
    color: int,
    separator: str = " ",
    gif_separator: str | None = None,
    include_gif: bool = True,
) -> discord.Embed:
    """Build an embed showing an image asset and links to its supported formats."""
    formats = [
        ("PNG", asset.replace(format="png")),
        ("JPG", asset.replace(format="jpg")),
        ("WEBP", asset.replace(format="webp")),
    ]
    has_gif = include_gif and asset.is_animated()
    if has_gif:
        formats.append(("GIF", asset.replace(format="gif")))

    link_separator = gif_separator if has_gif and gif_separator is not None else separator
    description = link_separator.join(f"[{label}]({url})" for label, url in formats)

    embed = discord.Embed(description=description, color=color, title=title)
    embed.set_image(url=asset.url)
    return embed
