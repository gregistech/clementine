import discord
class Command(object):
    func = ""
    perms = ""
    def __init__(self, func, perms=discord.Permissions(permissions=0)):
        self.func = func
        self.perms = perms
