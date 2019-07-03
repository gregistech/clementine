import discord
from music_downloader import *
queued_songs = []
async def is_connected_vc(voice_clients, current_guild):
    for x in voice_clients:
        if x.guild == current_guild:
            return x
    return False
def music_end_wrapper(voice_client):
    coro = on_music_ended(voice_client)
    fut = asyncio.run_coroutine_threadsafe(coro, client.loop)
    fut.result()
async def connect_play(music_id, voice_client):
    audio_source = discord.FFmpegPCMAudio("./music/{id}.mp3".format(id=music_id))
    voice_client.play(audio_source, after=lambda: music_end_wrapper(voice_client))
async def get_local_thumbnail(thmb_id):
    with open("./music/{image}".format(image=thmb_id + ".jpg"), "rb") as f:
        return discord.File(fp=f)
async def on_music_ended(voice_client):
    if len(queued_songs) == 0:
        print("asd" + str(len(queued_songs)))
        print(queued_songs)
        return
    music_id = queued_songs[len(queued_songs) - 1]
    music_info = await extract_info_yt("https://www.youtube.com/watch?v={id}".format(id=music_id))
    await connect_play(music_id, voice_client)
    await create_np_music_embed(music_info["title"], music_info["uploader"], music_id)
    await remove_queue(music_id)
    return
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
async def remove_queue(music_id):
    queued_songs.pop(music_id)
    return
