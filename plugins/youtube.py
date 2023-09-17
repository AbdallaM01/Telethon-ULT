# Ultroid - UserBot
# Copyright (C) 2021-2023 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://www.github.com/TeamUltroid/Ultroid/blob/main/LICENSE/>.
"""
✘ Commands Available -

• `{i}yta <(youtube/any) link>`
   Download audio from the link.

• `{i}ytv <(youtube/any) link>`
   Download video  from the link.

• `{i}ytsa <(youtube) search query>`
   Search and download audio from youtube.

• `{i}ytsv <(youtube) search query>`
   Search and download video from youtube.
"""
from core.remote import rm
from utilities.tools import is_url_ok

from . import get_string, ultroid_cmd


@ultroid_cmd(
    pattern="yt(a|v|sa|sv)( (.*)|$)",
)
async def youtube_func(event):
    with rm.get("ytdl", helper=True, dispose=True) as mod:
        download_yt, get_yt_link = mod.download_yt, mod.get_yt_link
    ytd = {
        "prefer_ffmpeg": True,
        "addmetadata": True,
        "geo-bypass": True,
        "nocheckcertificate": True,
        "postprocessors": [{"key": "FFmpegMetadata"}],
    }
    opt = event.pattern_match.group(1)
    xx = await event.eor(get_string("com_1"))
    if opt == "a":
        ytd["format"] = "bestaudio"
        ytd["outtmpl"] = "%(id)s.m4a"
        ytd["postprocessors"][0]["preferredcodec"] = "mp4a"
        ytd["postprocessors"][0]["preferredquality"] = "128"
        url = event.pattern_match.group(3) if event.pattern_match.group(2) else None
        if not url:
            return await xx.eor(get_string("youtube_1"))
        try:
            await is_url_ok(url)
        except BaseException:
            return await xx.eor(get_string("youtube_2"))
    elif opt == "v":
        ytd["format"] = "best"
        ytd["outtmpl"] = "%(id)s.mp4"
        ytd["postprocessors"][0]["preferredcodec"] = "avc1"
        url = event.pattern_match.group(3) if event.pattern_match.group(2) else None
        if not url:
            return await xx.eor(get_string("youtube_3"))
        try:
            await is_url_ok(url)
        except BaseException:
            return await xx.eor(get_string("youtube_4"))
    elif opt == "sa":
        ytd["format"] = "bestaudio"
        ytd["outtmpl"] = "%(id)s.m4a"
        ytd["postprocessors"][0]["preferredcodec"] = "mp4a"
        ytd["postprocessors"][0]["preferredquality"] = "128"
        query = event.pattern_match.group(3) if event.pattern_match.group(2) else None
        if not query:
            return await xx.eor(get_string("youtube_5"))
        url = get_yt_link(query, ytd)
        if not url:
            return await xx.edit(get_string("unspl_1"))
        await xx.eor(get_string("youtube_6"))
    elif opt == "sv":
        ytd["format"] = "best"
        ytd["outtmpl"] = "%(id)s.mp4"
        ytd["postprocessors"][0]["preferredcodec"] = "avc1"
        query = event.pattern_match.group(3) if event.pattern_match.group(2) else None
        if not query:
            return await xx.eor(get_string("youtube_7"))
        url = get_yt_link(query, ytd)
        if not url:
            return await xx.edit(get_string("unspl_1"))
        await xx.eor(get_string("youtube_8"))
    else:
        return
    await download_yt(xx, url, ytd)
