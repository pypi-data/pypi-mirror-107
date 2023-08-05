# Lion-X - UserBot
# Copyright (C) 2020 TeamLion-X
#
# This https://github.com/TeamLion-X/Lion-x is a part of < https://github.com/TeamLion-X/Lion-x/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamLion-X/Lion-x/blob/main/LICENSE/>.

import os
import time

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL import Image
from telethon.tl.types import DocumentAttributeAudio, DocumentAttributeVideo
from youtubesearchpython.__future__ import VideosSearch

from .all import uploader

# search youtube


async def get_yt_link(query):
    vid_ser = VideosSearch(query, limit=1)
    res = await vid_ser.next()
    results = res["result"]
    for i in results:
        link = i["link"]
    return link


async def download_yt(xx, event, link, ytd):
    st = time.time()
    info = ytd.extract_info(link, False)
    title = info["title"]
    author = info["uploader"]
    try:
        ytd.download([link])
    except Exception as e:
        return await xx.edit(f"**ERROR**:\n`{e}`")
    dir = os.listdir()
    if f"{info['id']}.mp3" in dir:
        tm = f"{info['id']}.mp3"
        os.rename(tm, f"{title}.mp3")
        kk = f"{title}.mp3"
        if f"{tm}.jpg" in dir:
            thumb = f"{tm}.jpg"
        elif f"{tm}.webp" in dir:
            thumb = f"{tm}.webp"
        else:
            thumb = "resources/extras/Lion.jpg"
        caption = f"`{title}`\n`From YouTubeMusic`"
    elif f"{info['id']}.mp4" in dir:
        os.rename(f"{info['id']}.mp4", f"{title}.mkv")
        kk = f"{title}.mkv"
        tm = f"{info['id']}"
        if f"{tm}.jpg" in dir:
            thumb = f"{tm}.jpg"
        elif f"{tm}.webp" in dir:
            thumb = f"{tm}.webp"
        else:
            thumb = "resources/extras/Lion.jpg"
        caption = f"`{title}`\n\n`From YouTube Official`"
    else:
        return
    res = await uploader(kk, kk, st, xx, "Uploading...")
    metadata = extractMetadata(createParser(res.name))
    wi = 512
    hi = 512
    duration = 0
    if metadata.has("width"):
        wi = metadata.get("width")
    if metadata.has("height"):
        hi = metadata.get("height")
    if metadata.has("duration"):
        duration = metadata.get("duration").seconds
    if kk.endswith(".mkv"):
        im = Image.open(thumb)
        ok = im.resize((int(wi), int(hi)))
        ok.save(thumb, format="PNG", optimize=True)
        await event.client.send_file(
            event.chat_id,
            file=res,
            caption=caption,
            attributes=[
                DocumentAttributeVideo(
                    duration=duration,
                    w=wi,
                    h=hi,
                    supports_streaming=True,
                )
            ],
            thumb=thumb,
        )
    else:
        await event.client.send_file(
            event.chat_id,
            file=res,
            caption=caption,
            supports_streaming=True,
            thumb=thumb,
            attributes=[
                DocumentAttributeAudio(
                    duration=duration,
                    title=title,
                    performer=author,
                )
            ],
        )
    os.remove(kk)
    os.remove(thumb)
    await xx.delete()
