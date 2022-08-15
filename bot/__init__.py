import logging
import os

from pyrogram import Client, __version__
from pyrogram.raw.all import layer

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
LOGGER = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)


class ENV_VARS(object):
    API_ID = int(os.environ.get("API_ID"))
    API_HASH = os.environ.get("API_HASH")
    BIFM_URL = os.environ.get("BIFM_URL", "https://bifm.tacohitbox.com/api/bypass?url")
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    BOT_USERNAME = os.environ.get("BOT_USERNAME")
    LANGUAGE = os.environ.get("LANGUAGE", "EN")
    AUTH_USERS = set(int(x) for x in os.environ.get("AUTH_USER", "").split())
    AUTH_USER = list(AUTH_USERS)
    MAX_MESSAGE_LENGTH = int(os.environ.get("MAX_MESSAGE_LENGTH", 4096))
    SENDER = os.environ.get("EMAIL") # Sender Email/Your Email
    PASSWORD = os.environ.get("PASSWORD") # Your Email's Password


Config = ENV_VARS
handler = Config.BOT_USERNAME


class CMD(object):
    START = ["start", f"start@{handler}"]
    ATSN = ["artstation", f"artstation@{handler}"]
    BIFM = ["bifm", f"bifm@{handler}"]
    DPLK = ["droplink", f"droplink@{handler}"]
    GPLK = ["gplink", f"gplink@{handler}"]
    MDIK = ["mdisk", f"mdisk@{handler}"]
    WETR = ["wetransfer", f"wetransfer@{handler}"]
    TEML = ["term", f"term@{handler}"]
    RUNF = ["eval", f"eval@{handler}"]
    CD = ["cd", f"cd@{handler}"]
    FILES = ["my_files", f"my_files@{handler}"]
    IP = ["ip", f"ip@{handler}"]
    STATUS = ["stats", f"stats@{handler}"]
    LINK = ["link", f"link@{handler}"]
    EMAIL = ["email", f"email@{handler}"]
