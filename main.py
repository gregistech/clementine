import discord
from discord.ext import commands

import sys, traceback

import json

import os

with open('./config.json', 'r') as out:
    config = json.loads(out.read())

def get_prefix(bot, message):
    if not message.guild:
        return config['default']['prefix']
    
    with open('./config.json', 'r') as out:
        config = json.loads(out.read())
    try:    
        prefix = config[str(message.guild.id)]['prefix']
    except KeyError:
        prefix = config['default']['prefix']

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
