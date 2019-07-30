import discord
import typing
from discord.ext import commands

from classes.config_handler import config_handler

class ModCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='purge')
    @commands.has_role('Moderators')
    async def purge(self, ctx, *, limit:int):
        await ctx.channel.purge(limit=limit)
        await ctx.channel.send(f"I purged {limit} messages! I LIKE BURNING THINGS OKAY?!!", delete_after=config_handler.get_config(ctx.message.guild.id, "delt"))
   
    @commands.command(name='kick')
    @commands.has_role('Moderators')
    async def kick(self, ctx, member:discord.Member, *, reason:typing.Optional[str]=None):
        await member.kick(reason=reason)
        if not reason:
            reason = "I wanted it like this"
        await ctx.channel.send(f"I kicked {member.nick} because {reason}. I love kicking some, oh I can't say that anymore...", delete_after=config_handler.get_config(ctx.message.guild.id, "delt"))
    
    @commands.command(name='ban')
    @commands.has_role('Moderators')
    async def ban(self, ctx, member:discord.Member, *, reason:typing.Optional[str]=None):
        await member.ban(reason=reason)
        if not reason:
            reason = "this member created an imbalance."
        await ctx.channel.send(f"I banned {member.nick} because {reason}. :wink:", delete_after=config_handler.get_config(ctx.message.guild.id, "delt"))

    @commands.command(name='unban')
    @commands.has_role('Moderators')
    async def unban(self, ctx, mention:str, *, reason:typing.Optional[str]=None):
        member = discord.Object(id=mention.replace('<', '').replace('>', '').replace('@', ''))
        await ctx.guild.unban(member, reason=reason)
        if not reason:
            reason = "I'm not a feelingless robot."
        await ctx.channel.send(f"I banned {member.nick} because {reason}. No need to fear!", delete_after=config_handler.get_config(ctx.message.guild.id, "delt"))

    @commands.command(name='edit')
    @commands.has_role('Moderators')
    async def edit(self, ctx, member:discord.Member, key:str, *, value:str):
        await ctx.channel.send(f"I edited **{key}** on {member.mention} to **{value}**!", delete_after=config_handler.get_config(ctx.message.guild.id, "delt"))
        await member.edit(**{key:value})

def setup(bot):
    bot.add_cog(ModCog(bot))
