import discord
import asyncio
class Tab(object):
    message = ""
    owner = ""
    pages = {}
    currentPage = 0
    def __init__(self, message, owner, pages, currentPage=0):
        self.message = message
        self.owner = owner
        self.pages = pages
        self.currentPage = currentPage
async def create_tab(self, owner, pages, channel, currentPage=0):
    pages[currentPage].set_footer(text="Page {current}/{all}".format(current=currentPage+1, all=len(pages)))
    currMessage = await channel.send(embed=pages[currentPage], delete_after=self.delt)
    await currMessage.add_reaction("\U00002b05")
    await currMessage.add_reaction("\U000027a1")
    self.open_tabs[currMessage.id] = Tab(currMessage, owner, pages, currentPage)
    return self.open_tabs[currMessage.id]
async def change_tab_page(self, id, channel, page):
    tab = self.open_tabs.pop(id)
    await tab.message.delete()
    await create_tab(self, tab.owner, tab.pages, channel, page)
