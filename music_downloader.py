import youtube_dl
import asyncio
import os
class music_downloader:
    async def extract_info_music(url):
        options = {
            "format": "bestaudio/best",
            "extractaudio" : True,
            "audioformat" : "mp3",
            "outtmpl": "./music/nope.asd",
            "noplaylist" : True,
            "default_search": "auto",
            "writethumbnail": True
        }
        with youtube_dl.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=False)
        return info
    async def download_audio_music(url):
        options = {
            "format": "bestaudio/best",
            "extractaudio" : True,
            "audioformat" : "mp3",
            "outtmpl": "./music/{name}.mp3".format(name=(await music_downloader.extract_info_music(url))["id"]),
            "noplaylist" : True,
            "writethumbnail": True
        }
        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download([url])
        return
