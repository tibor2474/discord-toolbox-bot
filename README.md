# 🧰 Toolbox
Toolbox is a utility Discord bot for things you didn't know you would need one day. You can quickly set slowmode, age-restrict channels, get detailed information about a member or role, view raw messages via context menus, and a lot more!

Built with [discord.py](https://github.com/Rapptz/discord.py) v2.

## Setup
### Replit and Glitch
First clone the repo with the buttons on top, or manually on the site. Then head over to the secrets tab, create a new secret called `TOKEN`, and place your bot token in the value field. Install all the packages using the command below, and you're done!

### Source
Clone the repo, and install all the required packages with the command below. At least Python 3.10 is required!
```bash
pip3 install -r requirements.txt
```

Then create a `.env` file and set your bot token:
```env
TOKEN=your_bot_token_here
```

After that, run the bot with this command:
```bash
python3 main.py
```

## Features & Cogs
- **channel**: Manage channel settings such as slowmode, age-restriction (NSFW), user limits, and voice regions.
- **info**: Detailed information displays for servers, roles, and members.
- **members**: Avatars, server avatars, user banners, voice moving, and user context menu info (`Show info`).
- **message**: Message utilities including raw message extraction context menu (`Show raw message`).
- **permission**: Inspect member and role guild permissions.
- **thread**: Thread management (closing, archiving, locking, renaming, and thread slowmode).
- **logging**: Standardized dual logging (console and timestamped log files under `logs/` in UTC time).

## Configuration
You can customize the bot in [config.py](config.py). You can change embed colors, time formatting strings, and icons.

> All icons were provided by [Font Awesome](https://fontawesome.com/)!
