from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot import CMD
from bot.helpers import bypasser

# Buttons
START_BUTTONS = [
    [
        InlineKeyboardButton("Source ❤️", url="https://github.com/prono69"),
        InlineKeyboardButton("Sus Channel 🍆", url="https://t.me/TrulyRealNinja"),
    ],
    [InlineKeyboardButton("Author 👨", url="https://kirito.in")],
]


@Client.on_message(filters.command(CMD.START))
async def start(bot, update):
    await update.reply_text(
        text=f"<b>Konichiwa {update.from_user.first_name},I am OppaiRobot.</b>\n<i>I can do some things.</i> :)",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(START_BUTTONS),
    )


@Client.on_message(
    filters.command(CMD.ATSN)
    & filters.regex(r"artstation\.com/(?:artwork|projects)/([0-9a-zA-Z]+)")
)
async def atsn(bot, update):
    id = update.matches[0].group(1)
    ouo = bypasser.art_k(id)
    message = await update.reply_text(
        text=ouo, disable_web_page_preview=False, quote=True
    )


@Client.on_message(filters.command(CMD.DPLK) & filters.regex(r"https?://[^\s]+"))
async def dpkl(bot, update):
    url = update.matches[0].group(0)
    ouo = bypasser.droplink(url)
    message = await update.reply_text(
        text=ouo, disable_web_page_preview=True, quote=True
    )


@Client.on_message(filters.command(CMD.WETR) & filters.regex(r"https?://[^\s]+"))
async def wetr(bot, update):
    url = update.matches[0].group(0)
    ouo = bypasser.wetransfer(url)
    message = await update.reply_text(
        text=ouo, disable_web_page_preview=True, quote=True
    )


@Client.on_message(filters.command(CMD.GPLK) & filters.regex(r"https?://[^\s]+"))
async def gpkl(bot, update):
    url = update.matches[0].group(0)
    ouo = bypasser.gplinks(url)
    message = await update.reply_text(
        text=ouo, disable_web_page_preview=True, quote=True
    )


@Client.on_message(filters.command(CMD.MDIK) & filters.regex(r"https?://[^\s]+"))
async def mdik(bot, update):
    url = update.matches[0].group(0)
    ouo = bypasser.mdisk(url)
    message = await update.reply_text(
        text=ouo, disable_web_page_preview=True, quote=True
    )


@Client.on_message(filters.command(CMD.BIFM) & filters.regex(r"https?://[^\s]+"))
async def bif(bot, update):
    x = update.matches[0].group(0)
    url = bypasser.encod(x)
    ouo = bypasser.bifm(url)
    message = await update.reply_text(
        text=ouo, disable_web_page_preview=True, quote=True
    )


@Client.on_message(
    filters.command(["test"])
    & filters.regex(r"https?://[^\s]+"))
async def xy(bot, update):
    urlx = update.matches[0].group(0)
    kek = bypasser.xyz(urlx)
    message = await update.reply_text(
        text=kek, disable_web_page_preview=True, quote=True
    )
    
