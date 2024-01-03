import discord
import os
from discord.ext import commands
from config import bot_token, bot_time

# set intents
intents = discord.Intents.default()
intents.members = True
intents.presences = True

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

for f in os.listdir("./context_menus"):
    if f.endswith(".py"):
        try:
            bot.load_extension("context_menus." + f[:-3])
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


# logging
@bot.event
async def on_application_command(ctx: discord.ApplicationContext) -> None: #log command execution
    print((discord.utils.utcnow().strftime(f"[{bot_time}]")), f"User @{ctx.author.name} (ID:{ctx.author.id}) used the {ctx.command.name} command")

# error checks
@bot.event
async def on_application_command_error(ctx: discord.ApplicationContext, error) -> None: #log app command error
    if isinstance(error, commands.BotMissingPermissions): #bot has missing permissions
        return await ctx.respond("I don't have the correct permissions to do that.", ephemeral=True)

    elif isinstance(error, commands.MissingPermissions): #user doesn't have perms
        return await ctx.respond("You don't have the correct permissions to do that.", ephemeral=True)
        
    else: #or something else
        await ctx.respond("An error occured while executing the command.", ephemeral=True)
    raise error


bot.run(bot_token)




# TODO:
# view server stats (count of users/bots, emojis, etc) - done
# user stats - done
# view emojis/stickers - done (skipped stickers)
# user images in different formats - done
# server logo and banner in different formats - done
# set custom slowmode for channels - done
# create/delete webhooks - skipped
# set name and pfp for webhooks - skipped
# convert colors (ex. hex to rgb) - skipped, kinda pointless
# set permissions for roles - skipped, for better security
# set permissions for channels - skipped, same
# show permissions for a role - done
# add a help command - skipped, not really needed
# purge messages from a specific member
# configure vc channel user limit - done
# change region for voice channel - done
# change server verification level - skipped, for better security
# add commands for soundboard management
# manage threads