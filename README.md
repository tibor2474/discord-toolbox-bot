# Toolbox

[![Run on Replit](https://replit.com/badge/github/tibor2474/toolbox)](https://replit.com/github/tibor2474/toolbox)

Toolbox is a utility bot for Discord servers. It brings everyday moderation and server-inspection tools together in one place: manage channel settings and threads, move members between voice channels, inspect member, role, and server details, and view avatars, banners, and message contents.

The bot is built with [discord.py](https://github.com/Rapptz/discord.py) 2.x. Its commands are registered as Discord slash commands. It also adds message and member context-menu actions.

## Features

- Update channel slowmode, age restrictions, voice user limits, and voice regions.
- Archive, lock, reopen, rename, and set slowmode on threads.
- Move members between voice channels.
- View member, role, server, and permission details.
- Display user and server icons, avatars, banners, invite backgrounds, and server emoji.
- Inspect a message's raw contents from its context menu.
- Write UTC logs to the console and timestamped files in `logs/`.

## Commands

Commands with channel, thread, or member-management effects require the corresponding Discord permissions. Discord also only shows commands in contexts where they can be used.

| Command              | Purpose                                            |
|----------------------|----------------------------------------------------|
| `/slowmode`          | Set or disable slowmode for a channel.             |
| `/nsfw`              | Turn a channel's age-restricted setting on or off. |
| `/vclimit`           | Set the user limit for a voice channel.            |
| `/vcregion`          | Change a voice channel's region.                   |
| `/threadclose`       | Archive a thread; staff can optionally lock it.    |
| `/threadopen`        | Reopen an archived thread.                         |
| `/threadname`        | Rename a thread.                                   |
| `/threadslowmode`    | Set or disable thread slowmode.                    |
| `/vcmove`            | Move a member to a voice channel.                  |
| `/memberinfo`        | Show information about a server member.            |
| `/serverinfo`        | Show information about the server.                 |
| `/roleinfo`          | Show information about a role.                     |
| `/memberpermissions` | Show a member's permissions.                       |
| `/rolepermissions`   | Show a role's permissions.                         |
| `/avatar`            | Show a user's avatar.                              |
| `/serveravatar`      | Show a user's avatar for this server.              |
| `/banner`            | Show a user's banner, if available.                |
| `/servericon`        | Show the server icon.                              |
| `/serverbanner`      | Show the server banner.                            |
| `/serverbackground`  | Show the server invite background.                 |
| `/serveremojis`      | Show the server's custom emoji.                    |

Additional context-menu actions are available by right-clicking a member and choosing **Apps → Show info**, or right-clicking a message and choosing **Apps → Show raw message**.

## Prerequisites

- Python 3.10 or newer.
- A Discord application and bot token from the [Discord Developer Portal](https://discord.com/developers/applications).
- A Discord server where you can add the bot. Invite it with the permissions required by the commands you intend to use; the bot needs the relevant channel, thread, and member permissions to perform those actions.

## Setup

### Run locally

1. Clone this repository and enter its directory.
2. (Recommended) Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

   On Windows, activate it with `.venv\\Scripts\\activate`.
3. Install dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```
4. Create a `.env` file in the project root and add your bot token:

   ```env
   TOKEN=your_discord_bot_token
   ```
5. Start the bot:

   ```bash
   python main.py
   ```

On startup, the bot loads its cogs and synchronizes its slash commands with Discord. Keep the token private; do not commit `.env` or share the token publicly.

### Run on Replit

Use the **Run on Replit** button at the top of this README to import the repository. In Replit, add a secret named `TOKEN` containing your Discord bot token, then install the packages from `requirements.txt` and run `python main.py`.

### Optional configuration

`config.py` loads `.env` automatically. You can set `BOT_COLOR` to a six-digit hexadecimal color (with or without a leading `#`) to customize embed accents:

```env
BOT_COLOR=#b4befe
```

## Project layout

- `main.py` starts the bot, loads extensions from `cogs/`, synchronizes application commands, and configures logging.
- `cogs/` contains command groups.
- `config.py` reads the token and optional embed color.
- `utils/` contains shared embed and permission helpers.
- `logs/` receives timestamped log files at runtime.

## Dependencies

Dependencies are listed in [`requirements.txt`](requirements.txt): `discord.py` and `python-dotenv`.
