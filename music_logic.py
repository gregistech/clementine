import discord
from music_downloader import *
queued_songs = []
async def is_connected_vc(voice_clients, current_guild):
    for x in voice_clients:
        if x.guild == current_guild:
            return x
    return False
def music_end_wrapper(error, voice_client, self):
    coro = on_music_ended(voice_client, self)
    fut = asyncio.run_coroutine_threadsafe(coro, self.loop)
    try:
        fut.result()
    except:
        pass
async def connect_play(music_id, voice_client, self):
    audio_source = discord.FFmpegPCMAudio("./music/{id}.mp3".format(id=music_id))
    voice_client.play(audio_source, after=lambda error: music_end_wrapper(error, voice_client, self))
async def get_local_thumbnail(thmb_id):
    with open("./music/{image}".format(image=thmb_id + ".jpg"), "rb") as f:
        return discord.File(fp=f)
async def on_music_ended(voice_client, self):
    if len(queued_songs) == 0:
        return
    music_id = queued_songs[0]
    url = "https://www.youtube.com/watch?v={id}".format(id=music_id)
    music_info = await extract_info_yt(url)
    await remove_queue()
    await connect_play(music_id, voice_client, self)
async def create_np_music_embed(title, uploader, music_id):
    info_embed = discord.Embed(title=title, description=uploader)
    info_embed.set_image(url="attachment://" + music_id + ".jpg")
    info_embed.set_footer(text="Currently playing")
    return info_embed
async def create_q_music_embed(title, uploader, music_id):
    info_embed = discord.Embed(title=title, description=uploader)
    info_embed.set_image(url="attachment://" + music_id + ".jpg")
    info_embed.set_footer(text="Queued {music_place}/{all_music}".format(music_place=len(queued_songs) - 1 - queued_songs[::-1].index(music_id) + 1, all_music=len(queued_songs)))
    return info_embed
async def add_queue(music_id):
    queued_songs.append(music_id)
    return
async def remove_queue():
    del queued_songs[0]
    return
