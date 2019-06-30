import discord
import math
import aiohttp
from io import BytesIO
from PIL import Image, ImageFilter
from tabs import *
from datetime import datetime
from json_handler import *
async def kick_user(self, message, params):
    if len(message.mentions) != 0:
        reason = ""
        for i in params:
            if "@" not in i:
                reason += i + " "
        for user in message.mentions:
            try:
                await user.kick(reason=reason)
            except discord.errors.Forbidden:
                await message.channel.send("{0} cannot be kicked because I don't have enough permission!".format(user.mention), delete_after=await self.get_config_value("delt", message.guild.id))
            else:
                if reason != "":
                    await message.channel.send("{0} kicked {1} from the server. Reason: {2}".format(message.author.mention, user.mention, reason), delete_after=await self.get_config_value("delt", message.guild.id))
                else:
                    await message.channel.send("{0} kicked {1} from the server. Reason: None".format(message.author.mention, user.mention), delete_after=await self.get_config_value("delt", message.guild.id))
    else:
        await message.channel.send("{mention}, you need to specify who you want to kick!".format(mention=message.author.mention), delete_after=await self.get_config_value("delt", message.guild.id))
async def ban_user(self, message, params):
    if len(message.mentions) != 0:
        reason = ""
        for i in params:
            if "@" not in i:
                reason += i + " "
        for user in message.mentions:
            try:
                await user.ban(reason=reason)
            except discord.errors.Forbidden:
                await message.channel.send("{0} cannot be banned because I don't have enough permission!".format(user.mention), delete_after=await self.get_config_value("delt", message.guild.id))
            else:
                if reason != "":
                    await message.channel.send("{0} banned {1} from the server. Reason: {2}".format(message.author.mention, user.mention, reason), delete_after=await self.get_config_value("delt", message.guild.id))
                else:
                    await message.channel.send("{0} banned {1} from the server. Reason: None".format(message.author.mention, user.mention), delete_after=await self.get_config_value("delt", message.guild.id))
    else:
        await message.channel.send("{mention}, you need to specify who you want to ban!".format(mention=message.author.mention), delete_after=await self.get_config_value("delt", message.guild.id))
async def help(self, message, params):
    pages = {}
    pages[0] = discord.Embed(title="Help for the help command")
    pages[0].set_author(name=message.author.name, icon_url=message.author.avatar_url)
    pages[0].add_field(name="command", value="*description* (command *required arguments* [*optional arguments*])")
    pages[1] = discord.Embed(title="Information commands")
    pages[1].set_author(name=message.author.name, icon_url=message.author.avatar_url)
    pages[1].add_field(name="help", value="I help you as I can, にゃあ~~! (help)")
    pages[1].add_field(name="latency", value="I can tell you my LATENCY! (latency [precise])")
    pages[1].add_field(name="about", value="I can tell everything ABOOUUUTT MYYYYYSEEEELLLLFFF *awkward singing noises* (about)")
    pages[2] = discord.Embed(title="Moderation commands")
    pages[2].set_author(name=message.author.name, icon_url=message.author.avatar_url)
    pages[2].add_field(name="kick", value="I can kick some... you know! (kick @spam @eggs [Some reasoning...])")
    pages[2].add_field(name="ban", value="This is the most painful thing I can to do someone... (ban @eggs @spam @KaTsUzU [Some seasoning, I mean reasoning!])")
    pages[3] = discord.Embed(title="Image manipulation commands")
    pages[3].set_author(name=message.author.name, icon_url=message.author.avatar_url)
    pages[3].add_field(name="gs_image", value="Do you hate colors, but you make an exception for black and white? This is your command! (gs_image https://example.page/example.png)")
    pages[3].add_field(name="blur_image", value="Do you want a cool blur effect, or you want to hide something? Well I'm here for your service! (It's Gaussian blur) (blur_image https://example.image [radius])")
    pages[4] = discord.Embed(title="Bot commands")
    pages[4].set_author(name=message.author.name, icon_url=message.author.avatar_url)
    pages[4].add_field(name="configure", value="Do you want to change some preferences? I can certainly help with that! (configure prefix .)")
    currTab = await create_tab(self, message.author, pages, message.channel)
async def latency(self, message, params):
    if len(params) != 0 and params[0] == "precise":
        latency = self.latency * 1000
    else:
        latency = math.ceil((self.latency * 1000) * 100)/100
    await message.channel.send("Well, the latency is: {0}ms!".format(latency), delete_after=await self.get_config_value("delt", message.guild.id))
async def about(self, message, params):
    aboutEmbed = discord.Embed(title="Hi! I'm going to introduce myself!")
    aboutEmbed.set_author(name=self.user.name, icon_url=self.user.avatar_url)
    aboutEmbed.add_field(name="What is my purpose?", value="Oh, I'm a multi-purpose bot! My mission is to entertain, defend and moderate communities!")
    aboutEmbed.add_field(name="Who is my creator?", value="I was written by {author}. He is the smartest, most beautiful, living human in the world. (His ego is reaaaaaally tiny. Right? RIGHT?!!!)".format(author=self.bot_info.owner.mention))
    await message.channel.send(embed=aboutEmbed, delete_after=await self.get_config_value("delt", message.guild.id))
async def gs_image(self, message, params):
    if len(params) >= 1:
        try:
            async with aiohttp.ClientSession() as client_session:
                async with client_session.get(params[0]) as response:
                    image_bytes = await response.read()
        except aiohttp.client_exceptions.InvalidURL:
            await message.channel.send("I can read everyone's mind, but uhhh, I can't guess the image on {0} address. :cry:".format(params[0]), delete_after=await self.get_config_value("delt", message.guild.id))
            return
        with Image.open(BytesIO(image_bytes)) as my_image:
            output_buffer = BytesIO()
            my_image = my_image.convert("L")
            my_image.save(output_buffer, "png")
            output_buffer.seek(0)
    await message.channel.send("As you wished I converted the image to grayscale! :upside_down:", file=discord.File(fp=output_buffer, filename="gs.png"))
async def blur_image(self, message, params):
    if len(params) >= 1:
        r = 2
        try:
            if len(params) >= 2:
                r = float(params[1])
        except ValueError:
            await message.channel.send("Well, I'm smart but I can't set the radius to {0}... :crying_cat_face:".format(params[1]), delete_after=await self.get_config_value("delt", message.guild.id))
            return
        try:
            async with aiohttp.ClientSession() as client_session:
                async with client_session.get(params[0]) as response:
                    image_bytes = await response.read()
        except aiohttp.client_exceptions.InvalidURL:
            await message.channel.send("I can read everyone's mind, but uhhh, I can't guess the image on {0} address. :cry:".format(params[0]), delete_after=await self.get_config_value("delt", message.guild.id))
            return
        with Image.open(BytesIO(image_bytes)) as my_image:
            output_buffer = BytesIO()
            my_image = my_image.filter(ImageFilter.GaussianBlur(r))
            my_image.save(output_buffer, "png")
            output_buffer.seek(0)
    await message.channel.send("As you wished I blured your image! :thinking: (What would you want to hide?)", file=discord.File(fp=output_buffer, filename="gs.png"))
    return
async def change_config(self, message, params):
    if len(params) >= 2:
        await change_config_value(params[0], params[1], message.guild.id)

