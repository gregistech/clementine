import youtube_dl
import asyncio
import os

async def extract_info_yt(url):
    options = {
        'format': 'bestaudio/best',
        'extractaudio' : True,
        'audioformat' : "mp3",
        'outtmpl': "./music/nope.asd",
        'noplaylist' : True,
    }
    with youtube_dl.YoutubeDL(options)  as ydl:
        info = ydl.extract_info(url, download=False)
    return info
async def download_audio_yt(url):
    options = {
        'format': 'bestaudio/best',
        'extractaudio' : True,
        'audioformat' : "mp3",
        'outtmpl': "./music/{name}.mp3".format(name=(await extract_info_yt(url))["id"]),
        'noplaylist' : True,
        "writethumbnail": True
    }
    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([url])
    return
