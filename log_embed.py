import discord
from datetime import datetime
class log_embed(object):  
    def __init__(self, title, desc, colour, timestamp, author):
        self.title = title
        self.desc = desc
        self.colour = colour
        self.timestamp = timestamp
        self.author = author
 
    def default(self):
        return log_embed("Unknown action", "Operation: Kill all humans", discord.Colour.green(), datetime(2100, 11, 26), self.user)
