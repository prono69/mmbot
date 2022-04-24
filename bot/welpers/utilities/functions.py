import asyncio
import math
import os
import shlex
import shutil
import time
from datetime import datetime
from time import time
from typing import Tuple
from urllib.error import HTTPError
from urllib.parse import unquote

import httpx
import psutil as p
import speedtest
from pySmartDL import SmartDL

SIZE_UNITS = ["B", "KB", "MB", "GB", "TB", "PB"]


def str_uptime(secs: float):
    if secs > 217728000:  # 1 year in secs
        return datetime.fromtimestamp(secs).strftime("%YY %mM %dd | %Hh %Mm %Ss")
    elif secs > 2629746:  # 1 month in secs
        return datetime.fromtimestamp(secs).strftime("%mM %dd | %Hh %Mm %Ss")
    else:  # 1 day in secs
        return datetime.fromtimestamp(secs).strftime("%dd | %Hh %Mm %Ss")


def ip() -> str:
    url = "http://ip-api.com/json/"
    data = httpx.get(url).json()
    IP = data["query"]
    ISP = data["isp"]
    Organisation = data["org"]
    country = data["country"]
    City = data["city"]
    Region = data["region"]
    Longitude = data["lon"]
    Latitude = data["lat"]
    Timezone = data["timezone"]
    zip_code = data["zip"]

    text = f"""
**My IP:** {IP}
**ISP:** {ISP}
**Organisation:** {Organisation}
**Country:** {country}
**City:** {City}
**Region:** {Region}
**Longitude:** {Longitude}
**Latitude:** {Latitude}
**Time zone:** {Timezone}
**Zip code:** {zip_code}
"""
    return text


def get_server_details():

    dtotal, dused, dfree = shutil.disk_usage(".")
    mem = p.virtual_memory()
    tram, aram, uram, fram, fpercent = (
        mem.total,
        mem.available,
        mem.used,
        mem.free,
        mem.percent,
    )

    cpuf = p.cpu_freq()
    ccpu, mcpu = cpuf.current, cpuf.max

    lcore, pcore = p.cpu_count(logical=True), p.cpu_count(logical=False)

    text = f""" **System Details **

__Storage__
  Total: {humanbytes(dtotal)}
  Used: {humanbytes(dused)}
  Free: {human_readable_speed(dfree)}

__Core & Cpu Info__
  CPU Frequency: {ccpu} Mhz
  Max: {mcpu}
  PCore: {pcore} LCore: {lcore}

__Ram Info__
  Total: {humanbytes(tram)}
  Available: {humanbytes(aram)}
  Used: {human_readable_speed(uram)}
  Free: {humanbytes(fram)}
  Usage: {fpercent}%

  Uptime: {str_uptime(time() - p.boot_time())}
  Booted on: {datetime.fromtimestamp(p.boot_time()).strftime("%Y-%m-%d %H:%M:%S")}
  Stats as of: {datetime.fromtimestamp(time()).strftime("%Y-%m-%d %H:%M:%S")}
 """

    return text


def get_server_speedtest():
    speedy = speedtest.Speedtest()
    speedy.get_best_server()
    speedy.download()
    speedy.upload()
    speedy.results.share()
    speedresult = speedy.results.dict()
    image_url = speedresult["share"]
    speedstring = f"""__Server SpeedTest Result__
**Server Details**

__Name__:**{speedresult['server']['name']}**
__Country__:**{speedresult['server']['country']}**,**{speedresult['server']['cc']}**
__Sponser__:**{speedresult['server']['sponsor']}**

__**Speed Results**__
__Ping__:**{speedresult['ping']}**
__Upload__:**{humanbytes(speedresult['upload'] / 8)}/s**
__Download__:**{humanbytes(speedresult['download'] / 8)}/s**
__ISP__:**{speedresult['client']['isp']}**
"""
    return speedstring, image_url


def human_readable_speed(size):
    power = 2**10
    zero = 0
    units = {0: "", 1: "Kb", 2: "MB", 3: "Gb", 4: "Tb"}
    while size > power:
        size /= power
        zero += 1
    return f"{round(size, 2)} {units[zero]}"


def get_readable_time(seconds: int) -> str:
    result = ""
    (days, remainder) = divmod(seconds, 86400)
    days = int(days)
    if days != 0:
        result += f"{days}d"
    (hours, remainder) = divmod(remainder, 3600)
    hours = int(hours)
    if hours != 0:
        result += f"{hours}h"
    (minutes, seconds) = divmod(remainder, 60)
    minutes = int(minutes)
    if minutes != 0:
        result += f"{minutes}m"
    seconds = int(seconds)
    result += f"{seconds}s"
    return result


def humanbytes(size_in_bytes) -> str:
    if size_in_bytes is None:
        return "0B"
    index = 0
    while size_in_bytes >= 1024:
        size_in_bytes /= 1024
        index += 1
    try:
        return f"{round(size_in_bytes, 2)}{SIZE_UNITS[index]}"
    except IndexError:
        return "File too large"


# https://github.com/MysteryBots/UnzipBot/blob/0bc500639ceb18492ac89c8a9de1b8d87241c3cd/UnzipBot/functions.py#L17
async def absolute_paths(directory):
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            yield os.path.abspath(os.path.join(dirpath, f))


# https://github.com/X-Gorn/FridayUB/blob/90814701558e986a68fdec2776c5aa004caa8ca5/main_startup/helper_func/basic_helpers.py#L378
async def runcmd(cmd: str) -> Tuple[str, str, int, int]:
    """run command in terminal"""
    args = shlex.split(cmd)
    process = await asyncio.create_subprocess_exec(
        *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return (
        stdout.decode("utf-8", "replace").strip(),
        stderr.decode("utf-8", "replace").strip(),
        process.returncode,
        process.pid,
    )


async def progress_for_pyrogram(current, total, ud_type, message, start):
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        # if round(current / total * 100, 0) % 5 == 0:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion

        elapsed_time = TimeFormatter(milliseconds=elapsed_time)
        estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)

        progress = "[{0}{1}] \nP: {2}%\n".format(
            "".join(["█" for i in range(math.floor(percentage / 5))]),
            "".join(["░" for i in range(20 - math.floor(percentage / 5))]),
            round(percentage, 2),
        )

        tmp = progress + "{0} of {1}\nSpeed: {2}/s\nETA: {3}\n".format(
            humanbytes(current),
            humanbytes(total),
            humanbytes(speed),
            # elapsed_time if elapsed_time != '' else "0 s",
            estimated_total_time if estimated_total_time != "" else "0 s",
        )
        try:
            await message.edit(text="{}\n {}".format(ud_type, tmp))
        except BaseException:
            pass


def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        ((str(days) + "d, ") if days else "")
        + ((str(hours) + "h, ") if hours else "")
        + ((str(minutes) + "m, ") if minutes else "")
        + ((str(seconds) + "s, ") if seconds else "")
        + ((str(milliseconds) + "ms, ") if milliseconds else "")
    )
    return tmp[:-2]


# https://github.com/viperadnan-git/google-drive-telegram-bot/blob/main/bot/helpers/downloader.py
def download_file(url, dl_path):
    try:
        dl = SmartDL(url, dl_path, progress_bar=False)
        dl.start()
        filename = dl.get_dest()
        if "+" in filename:
            xfile = filename.replace("+", " ")
            filename2 = unquote(xfile)
        else:
            filename2 = unquote(filename)
        os.rename(filename, filename2)
        return True, filename
    except HTTPError as error:
        return False, error
