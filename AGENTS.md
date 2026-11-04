# AGENTS.md

## Project overview

Toolbox is a Python Discord utility bot built on `discord.py` 2.x. `main.py` creates the bot, loads every Python extension in `cogs/`, syncs application commands, and configures UTC console and file logging. `cogs/` contains slash commands and context-menu actions; `utils/` contains shared embed and permission helpers. `config.py` loads `.env` values.

## Setup and run

- Requires Python 3.10 or newer.
- Create a virtual environment with `python3 -m venv .venv` and activate it (`source .venv/bin/activate` on Unix, `.venv\\Scripts\\activate` on Windows).
- Install dependencies with `python -m pip install -r requirements.txt`.
- Set `TOKEN` in the environment or a root `.env` file. Optionally set `BOT_COLOR` to a six-digit hex color, with or without `#`.
- Run locally with `python main.py`. Startup requires a valid Discord bot token and network access; it loads cogs and synchronizes commands with Discord.
- Build the container with `docker build -t toolbox .`; run it with `docker run --rm -e TOKEN=... -v toolbox-logs:/app/logs toolbox` (pass `BOT_COLOR` with another `-e` if needed).

Keep bot credentials out of source control. `config.py` exposes the token as `BOT_TOKEN` and the embed accent as `BOT_COLOR`.

## Code organization and conventions

- Add bot commands in a suitable module under `cogs/`. Each cog is a `commands.Cog` and exposes an async `setup(bot)` function that adds the cog; `main.py` discovers `.py` files there automatically.
- Use `discord.app_commands` decorators for slash commands and keep command descriptions, parameter descriptions, and permission/context restrictions explicit.
- Put reusable embed or permission formatting in `utils/` rather than duplicating it across cogs. Import shared settings from `config.py`.
- Follow the existing Python style: four-space indentation, type annotations on public helpers and command callbacks, docstrings for modules/classes/functions, and `snake_case` names. Use `discord.Embed` and respond through the interaction response/followup API.
- For commands that modify server state, check the relevant Discord permissions and handle guild-only context. Keep user-facing error responses ephemeral where appropriate.

## Verification

There is currently no test suite, test configuration, or lint/format command in the repository. No automated checks are defined. For changes, inspect the affected code and run `python -m compileall main.py config.py cogs utils` for syntax validation. Running the bot additionally requires a configured token and Discord access; it synchronizes commands remotely.

## Runtime and deployment notes

- Logs are written to the console and to timestamped files in `logs/`; the Docker image declares `/app/logs` as a volume.
- The Dockerfile uses a multi-stage build based on Python 3.14 Alpine.
- Keep `requirements.txt` as the source of Python runtime dependencies and update it when adding an import dependency.
- Slash-command synchronization happens at startup, so avoid launching multiple instances casually during command changes.
