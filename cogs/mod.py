import discord
import typing
from discord.ext import commands

class ModCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='purge')
    @commands.has_role('Moderators')
    async def purge(self, ctx, *, limit:int):
        await ctx.channel.purge(limit=limit)
    
    @commands.command(name='kick')
    @commands.has_role('Moderators')
    async def kick(self, ctx, member:discord.Member, *, reason:typing.Optional[str]=None):
        await member.kick(reason=reason)
    
    @commands.command(name='ban')
    @commands.has_role('Moderators')
    async def ban(self, ctx, member:discord.Member, *, reason:typing.Optional[str]=None):
        await member.ban(reason=reason)
    
    @commands.command(name='unban')
    @commands.has_role('Moderators')
    async def unban(self, ctx, mention:str, *, reason:typing.Optional[str]=None):
        member = discord.Object(id=mention.replace('<', '').replace('>', '').replace('@', ''))
        await ctx.guild.unban(member, reason=reason)
    
    @commands.command(name='edit')
    @commands.has_role('Moderators')
    async def edit(self, ctx, member:discord.Member, key:str, *, value:str):
        await member.edit(**{key:value})

def setup(bot):
    bot.add_cog(ModCog(bot))
