import discord
from discord.ext import commands

class UtilCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    

    @commands.command(name='roleinfo', aliases=["ri"])
    async def roleinfo(self, ctx, role:discord.Role):
        embed = discord.Embed(title="Role information", colour=role.colour, description=role.name)
        
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)

        embed.add_field(name="ID", value=role.id)
        embed.add_field(name="Permission value", value=role.permissions.value)
        embed.add_field(name="Hoist", value=role.hoist)
        embed.add_field(name="Position", value=role.position)
        embed.add_field(name="Managed", value=role.managed)        
        await ctx.channel.send(embed=embed)



def setup(bot):
    bot.add_cog(UtilCog(bot))
