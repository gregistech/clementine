import traceback
import sys
from discord.ext import commands
import discord


class ErrorHandlerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'):
            return
        
        ignored = ()
        error = getattr(error, 'original', error)
        
        if isinstance(error, ignored):
            return

        elif isinstance(error, commands.DisabledCommand):
            return await ctx.send(f'{ctx.author.mention}! {ctx.command} has been disabled.')

        elif isinstance(error, commands.BadArgument):
            return await ctx.send(f'{ctx.author.mention}! You gave **bad arguments** to this command. Too bad... :facepalm:')
        
        elif isinstance(error, commands.CommandNotFound):
            return await ctx.send(f"{ctx.author.mention}! This **command doesn't exist**, but fear not! Just type in **{ctx.prefix}help**!")
        
        elif isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(f"{ctx.author.mention}! {str(error).capitalize()}")
        
        elif isinstance(error, discord.errors.Forbidden):
            return await ctx.send(f"{ctx.author.mention}! I don't have the permissions to do that, or you have to move my role higher up in the hierarchy!")

        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


def setup(bot):
    bot.add_cog(ErrorHandlerCog(bot))
