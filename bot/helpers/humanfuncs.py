# https://huzunluartemis.github.io/ChatSizeBot/

import math
from bot import LOGGER, Config

def humanbytes(size):
    size = int(size)
    # https://stackoverflow.com/a/49361727/4723940
    # 2**10 = 1024
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'Ki', 2: 'Mi', 3: 'Gi', 4: 'Ti'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + 'B'

def TimeFormatter(milliseconds) -> str:
    milliseconds = int(milliseconds) * 1000
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "d, ") if days else "") + \
        ((str(hours) + "h, ") if hours else "") + \
        ((str(minutes) + "m, ") if minutes else "") + \
        ((str(seconds) + "s, ") if seconds else "") + \
        ((str(milliseconds) + "ms, ") if milliseconds else "")
    return tmp[:-2]

def get_progressbar(current=0, total=0):
    if current == 0 or total == 0:
        return "[{0}]".format(Config.FINISHED_PROGRESS_STR * Config.PROGRESSBAR_LENGTH)
    try:
        return "[{0}{1}]".format(
        ''.join([Config.FINISHED_PROGRESS_STR for i in range(math.floor(current * 100 / total / (100/Config.PROGRESSBAR_LENGTH)))]),
        ''.join([Config.UN_FINISHED_PROGRESS_STR for i in range(Config.PROGRESSBAR_LENGTH - math.floor(current * 100 / total / (100/Config.PROGRESSBAR_LENGTH)))])
        )
    except Exception as e:
        LOGGER.exception(e)
        return "[{0}]".format(Config.FINISHED_PROGRESS_STR * Config.PROGRESSBAR_LENGTH)