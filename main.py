import discord
import os
from discord.ext import commands
from config import bot_token, bot_time

intents = discord.Intents.default()
bot = commands.Bot(intents=intents, help_command=None)

# load commands
for f in os.listdir("./commands"):
    if f.endswith(".py"):
        try:
            bot.load_extension("commands." + f[:-3])
        except Exception as error:
            print((discord.utils.utcnow().strftime(f"[{bot_time}]")), f"ERROR {f} could not be loaded: {error}")
        else:
            print((discord.utils.utcnow().strftime(f"[{bot_time}]")),f"Loaded {f}")

# sync commands
@bot.event
async def on_connect():
    await bot.sync_commands(delete_existing=True)
    print((discord.utils.utcnow().strftime(f"[{bot_time}]")), "Synced commands")

@bot.event
async def on_ready():
    print((discord.utils.utcnow().strftime(f"[{bot_time}]")), f"Logged in as {bot.user}")

@bot.listen
async def on_message(message):
    if message.author == bot.user:
        return


bot.run(bot_token)




# TODO:
# view server stats (count of users/bots, emojis, etc)
# user stats
# view emojis/stickers
# user images in different formats
# server logo and banner in different formats
# set custom slowmode for channels
# create/delete webhooks
# set name and pfp for webhooks
# convert colors (ex. hex to rgb)
# set permissions for roles
# set permissions for channels