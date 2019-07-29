import discord
from discord.ext import commands

from classes.config_handler import config_handler

import sys, traceback
import os


def get_prefix(bot, message):
    if not message.guild:
        return config_handler.get_default_config
    prefix = config_handler.get_config(message.guild.id, "prefix")
    return commands.when_mentioned_or(*prefix)(bot, message)

def get_token():
    try:
        return os.environ['CLEMTOKEN']
    except KeyError:
        print("Set CLEMTOKEN environment variable to your bot token!")
        sys.exit()


initial_extensions = ["cogs.mod",
                      "cogs.error_handler",
                      "cogs.util"]

bot = commands.Bot(command_prefix=get_prefix, description='Multi-purpose discord bot!')

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)

@bot.event
async def on_ready():
    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')
    await bot.change_presence(activity=discord.Activity(name='your behaviour!', type=3))
    print(f'Successfully logged in and booted...!')

try:
    bot.run(get_token(), bot=True, reconnect=True)
except discord.errors.LoginFailure:
    print("Couldn't login for some reason! (Check CLEMTOKEN environment variable!)")
