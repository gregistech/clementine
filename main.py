import discord
import asyncio
import json
from command import command
from bot_func import *
from tabs import *
from json_handler import *
from log_embed import log_embed
from datetime import date, datetime

with open(config_filepath, "r") as out:
    config = json.loads(out.read())
token = config["token"]

async def log_action(self, message, action_type, reaction = 0):
    log_channel = self.get_channel(int(await self.get_config_value("log_channel", message.guild.id)))
    new_embed = log_embed.default(self)

    if action_type == "deleted_message":
        new_embed = log_embed("Deleted message", message.content, discord.Colour.dark_red(), datetime.now(), message.author)
    elif action_type == "deleted_reaction":
        new_embed = log_embed("Deleted reaction", "{content} | {emoji}".format(content=message.content, emoji=reaction.emoji), discord.Colour.dark_red(), datetime.now(), message.author)
    elif action_type == "edited_message":
        new_embed = log_embed("Edited message", "{before} -> {after}".format(before=reaction.content, after=message.content), discord.Colour.dark_red(), datetime.now(), message.author)
    
    log_message_embed = discord.Embed(title=new_embed.title, description=new_embed.desc, timestamp=new_embed.timestamp, colour=new_embed.colour)
    log_message_embed.set_author(name=new_embed.author, icon_url=new_embed.author.avatar_url)
    await log_channel.send(embed=log_message_embed)
 
class Client(discord.Client):
    open_tabs = {}      
    
    async def get_config_value(self, key, guild_id):
        config = await get_config_contents()
        try:
            value = config[str(guild_id)][str(key)]
            return value
        except KeyError:
            if key != "log_channel" and key != "starboard_channel":
                try:
                    value = config["default"][str(key)]
                    print("Warning: Needed to get key from the default config options! Guild ID: {0}".format(guild_id))
                    return value
                except KeyError:
                    raise KeyError("Config key doesn't exist!")
            else:
                for x in message.guild.channels:
                    if x.name == key:
                        return x.id

    async def on_ready(self):
        self.bot_info = await self.application_info()
        print("///=----------------------------------=///\nLogged in as {username} with ID {id}\n///=----------------------------------=///".format(username=self.user.name, id=self.user.id))
    commands = {"kick": command(kick_user, discord.Permissions(permissions=2)),
                "ban": command(ban_user, discord.Permissions(permissions=4)),
                "help": command(help),
                "latency": command(latency),
                "about": command(about),
                "gs_image": command(gs_image),
                "blur_image": command(blur_image),
                "configure": command(change_config, discord.Permissions(permissions=32)),
                "play": command(play),
                "skip": command(skip),
                "stop": command(stop)}

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
                    self.starboard_channel = self.get_channel(int(await self.get_config_value("starboard_channel", reaction.message.guild.id)))
                    starMessage = await self.starboard_channel.send(embed=starMessageEmbed)
                    await save_starboard(reaction.message.id, starMessage.id, reaction.count)

    async def on_reaction_remove(self, reaction, user):
        await log_action(self, reaction.message, "deleted_reaction", reaction)
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
        await log_action(self, message, "deleted_message")
    async def on_message_edit(self, before, after):
        if after.author == self.user:
            return
        if before.content != after.content:
            await log_action(self, after, "edited_message", before)

client = Client(activity=discord.Activity(name="your behaviour!", type=3))
client.run(token)
