import discord
from music_downloader import music_downloader
queued_songs = []
class music_logic:
    async def add_queue(music):
        queued_songs.append(music)
        return
    async def remove_queue():
        del queued_songs[0]
        return
    async def is_connected_vc(voice_clients, current_guild):
        for x in voice_clients:
            if x.guild == current_guild:
                return x
        return False
    def connect_play(music, voice_client, self):
        audio_source = discord.FFmpegPCMAudio("./music/{id}.mp3".format(id=music.id))
        voice_client.play(audio_source, after=lambda error: music_logic.on_music_ended(voice_client, self))
    def on_music_ended(voice_client, self):
        if len(queued_songs) == 0:
            return "no_queue"
        voice_client.stop()
        music = queued_songs[0]
        del queued_songs[0]
        music_logic.connect_play(music, voice_client, self)
        return "skipped"
    async def create_np_music_embed(music):
        title = music.title
        uploader = music.uploader
        music_id = music.id
        info_embed = discord.Embed(title=title, description=uploader)
        info_embed.set_image(url="attachment://" + music_id + ".jpg")
        info_embed.set_footer(text="Currently playing")
        return info_embed
    async def create_q_music_embed(music):
        title = music.title
        uploader = music.uploader
        music_id = music.id
        info_embed = discord.Embed(title=title, description=uploader)
        info_embed.set_image(url="attachment://" + music_id + ".jpg")
        info_embed.set_footer(text="Queued {music_place}/{all_music}".format(music_place=len(queued_songs) - 1 - queued_songs[::-1].index(music) + 1, all_music=len(queued_songs)))
        return info_embed
    async def params_to_searchterm(params):
        search_term = ""
        for i in params:
            search_term += " " + i
        return search_term[1::]
    async def get_local_thumbnail(thmb_id):
        with open("./music/{image}".format(image=thmb_id + ".jpg"), "rb") as f:
            return discord.File(fp=f)
