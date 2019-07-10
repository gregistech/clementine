import discord
from discord.ext import commands

import sys, traceback

import json

with open('./config.json', 'r') as out:
    config = json.loads(out.read())
token = config['token']

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


initial_extensions = ["cogs.mod",
                      "cogs.error_handler"]

bot = commands.Bot(command_prefix=get_prefix, description='Multi-purpose discord bot!')

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)

@bot.event
async def on_ready():
    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')

    await bot.change_presence(activity=discord.Activity(name='your behaviour!', type=3))
    print(f'Successfully logged in and booted...!')

bot.run(token, bot=True, reconnect=True)
