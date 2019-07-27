import discord
from discord.ext import commands

class UtilCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    

    @commands.command(name='roleinfo', aliases=['ri'])
    async def roleinfo(self, ctx, role:discord.Role):
        embed = discord.Embed(title='Role information', colour=role.colour, description=role.name)
        
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)

        embed.add_field(name='ID', value=role.id)
        embed.add_field(name='Permission value', value=role.permissions.value)
        embed.add_field(name='Hoist', value=role.hoist)
        embed.add_field(name='Position', value=role.position)
        embed.add_field(name='Managed', value=role.managed)        
        await ctx.channel.send(embed=embed)

    @commands.command(name='serverinfo', aliases=['si'])
    async def serverinfo(self, ctx):
        guild = ctx.message.guild
        
        embed = discord.Embed(title='Server/Guild information', description=guild.name)
        
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        
        embed.add_field(name='ID', value=guild.id)
        embed.add_field(name='Region', value=guild.region)
        embed.add_field(name='AFK timeout', value=guild.afk_timeout)
        embed.add_field(name='AFK channel', value=guild.afk_channel)
        embed.add_field(name='Max. presences', value=guild.max_presences)
        embed.add_field(name='Max. members', value=guild.max_members)
        embed.add_field(name='Description', value=guild.description)
        embed.add_field(name='2FA authorisation', value=guild.mfa_level)
        embed.add_field(name='Verification level', value=guild.verification_level)
        embed.add_field(name='Explicit content filter', value=guild.explicit_content_filter)
        embed.add_field(name='Notification settings', value=guild.default_notifications)
        embed.add_field(name='Premium tier', value=guild.premium_tier)
        embed.add_field(name='Nitro boosters', value=guild.premium_subscription_count)
        embed.add_field(name='Member count', value=guild.member_count)
        embed.add_field(name='Created at (UTC)', value=guild.created_at)
        await ctx.channel.send(embed=embed)



def setup(bot):
    bot.add_cog(UtilCog(bot))
