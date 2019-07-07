import discord
from discord.ext import commands

class ModCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    

    @commands.command(name='purge')
    @commands.has_role('Moderators')
    async def purge(self, ctx, *, limit : int):
        await ctx.channel.purge(limit=limit)

def setup(bot):
    bot.add_cog(ModCog(bot))
