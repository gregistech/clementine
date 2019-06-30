import discord
import asyncio
import json
from command import Command
from bot_func import *
from tabs import *
from json_handler import *

with open(config_filepath, "r") as out:
    config = json.loads(out.read())
token = config["token"]
class Client(discord.Client):
    open_tabs = {}
    async def get_config_value(self, key, guild_id):
        config = await get_config_contents()
        try:
            value = config[str(guild_id)][str(key)]
            return value
        except KeyError:
            try:
                value = config["default"][str(key)]
                print("Warning: Needed to get key from the default config options! Guild ID: {0}".format(guild_id))
                return value
            except KeyError:
                raise KeyError("Config key doesn't exist!")

    async def on_ready(self):
        self.bot_info = await self.application_info()
        print("///=----------------------------------=///\nLogged in as {username} with ID {id}\n///=----------------------------------=///".format(username=self.user.name, id=self.user.id))
    commands = {"kick": Command(kick_user, discord.Permissions(permissions=2)),
                "ban": Command(ban_user, discord.Permissions(permissions=4)),
                "help": Command(help),
                "latency": Command(latency),
                "about": Command(about),
                "gs_image": Command(gs_image),
                "blur_image": Command(blur_image),
                "configure": Command(change_config, discord.Permissions(permissions=32))}

    async def on_reaction_add(self, reaction, user):
        if user == self.user:
            return
        try:
            if user == self.open_tabs[reaction.message.id].owner:
                offset = 0
                if reaction.emoji == "➡":
                    if self.open_tabs[reaction.message.id].currentPage == len(self.open_tabs[reaction.message.id].pages) - 1:
                        offset = 0
                    else:
                        offset = 1
                elif reaction.emoji == "⬅":
                    if self.open_tabs[reaction.message.id].currentPage == 0:
                        offset = 0
                    else:
                        offset = -1
                else:
                    return
            await change_tab_page(self, reaction.message.id, reaction.message.channel, self.open_tabs[reaction.message.id].currentPage + offset)
            return
        except KeyError:
            if reaction.emoji == "👍":
                starboard = await get_starboard()
                if starboard != []:
                    for v in starboard:
                        if v["msgId"] == reaction.message.id:
                            await change_starboard(reaction.message.id, reaction.count)
                            return
                if reaction.count >= await self.get_config_value("minfsb", reaction.message.guild.id):
                    starMessageEmbed = discord.Embed(title="👍 " + str(reaction.count), description=str(reaction.message.content), timestamp=reaction.message.created_at)
                    starMessageEmbed.set_author(name=reaction.message.author, icon_url=reaction.message.author.avatar_url)
                    for x in reaction.message.guild.channels:
                        if x.name == "starboard":
                            self.starboard_channel = x
                            starMessage = await self.starboard_channel.send(embed=starMessageEmbed)
                            await save_starboard(reaction.message.id, starMessage.id, reaction.count)

    async def on_reaction_remove(self, reaction, user):
        if reaction.emoji == "👍":
                starboard = await get_starboard()
                if starboard != []:
                    for v in starboard:
                        if v["msgId"] == reaction.message.id:
                            await change_starboard(reaction.message.id, reaction.count)
                            if reaction.count < await self.get_config_value("minfsb", reaction.message.guild.id):
                                starMessage = await self.starboard_channel.fetch_message(int(v["starMsgId"]))
                                await starMessage.delete()
                                await remove_starboard(v["msgId"])
                            else:
                                starMessageEmbed = discord.Embed(title="👍 " + str(reaction.count), description=str(reaction.message.content), timestamp=reaction.message.created_at)
                                starMessageEmbed.set_author(name=reaction.message.author, icon_url=reaction.message.author.avatar_url)
                                for x in reaction.message.guild.channels:
                                    if x.name == "starboard":
                                        self.starboard_channel = x
                                        message = await self.starboard_channel.fetch_message(v["starMsgId"])
                                        starMessage = message.edit(starMessageEmbed)
                                        await save_starboard(reaction.message.id, starMessage.id, reaction.count)
                            return

    async def on_message(self, message):
        if message.author == self.user:
            return
        if message.content.startswith(await self.get_config_value("prefix", message.guild.id)):
            com, sep, params = message.content.partition(" ")
            com = com[1:]
            params = list(filter(None, params.split(" ")))
            try:
                v = self.commands[com]
            except KeyError:
                await message.channel.send("{mention}, try the **{pf}help** command, because this command doesn't exist!".format(mention=message.author.mention, pf=await self.get_config_value("prefix", message.guild.id)), delete_after=await self.get_config_value("delt", message.guild.id))
            else:
                if message.author.top_role.permissions >= v.perms:
                    await v.func(self, message, params)
                else:
                    await message.channel.send("{mention}, you don't have enough permission to do this!".format(mention=message.author.mention), delete_after=await self.get_config_value("delt", message.guild.id))
    async def on_message_delete(self, message):
        if message.author == self.user:
            return
        for x in message.guild.channels:
            if x.name == "logs":
                log_message_embed = discord.Embed(title="Deleted message", description=str(message.content), timestamp=message.created_at, colour=discord.Colour.dark_red())
                log_message_embed.set_author(name=message.author, icon_url=message.author.avatar_url)
                await x.send(embed=log_message_embed)

client = Client(activity=discord.Activity(name="your behaviour!", type=3))
client.run(token)
