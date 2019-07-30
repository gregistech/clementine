import discord
import typing
from discord.ext import commands

from classes.config_handler import config_handler

class ConfigCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='setconfig', aliases=["sc"])
    @commands.has_role('Moderators')
    async def set_config(self, ctx, key:str, *, value:str):
        config_handler.set_config(ctx.message.guild.id, key, value)
        await ctx.channel.send("I changed **{key}** to **{value}**!".format(key=key, value=value))

    
    @commands.command(name='getconfig', aliases=["gc"])
    @commands.has_role('Moderators')
    async def get_config(self, ctx, key:str):
        try:
            value = config_handler.get_config(ctx.message.guild.id, key)
        except:
            await ctx.channel.send("This key doesn't exist, baka!")
            return
        await ctx.channel.send("The key **{key}** equals to **{value}**!".format(key=key, value=value))
    
def setup(bot):
    bot.add_cog(ConfigCog(bot))
