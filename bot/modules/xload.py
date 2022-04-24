import os
import shutil
import time

from pyrogram import Client, filters
from pyrogram.errors import BadRequest
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from bot import AUTH_USER, Config
from bot.welpers.utilities.functions import *

CB_BUTTONS = [
    [
        InlineKeyboardButton("Zip", callback_data="zip"),
        InlineKeyboardButton("One by one", callback_data="1by1"),
    ]
]

# Helpers

if AUTH_USER:
    OWNER_FILTER = filters.chat(AUTH_USER) & filters.incoming
else:
    OWNER_FILTER = filters.incoming


@Client.on_message(filters.command("link") & OWNER_FILTER)
async def linkloader(bot, update):
    # xlink = await update.reply_text("Processing...")
    if Config.BUTTONS:
        return await update.reply_text(
            "You wanna upload files as?",
            True,
            reply_markup=InlineKeyboardMarkup(CB_BUTTONS),
        )
    elif Config.BUTTONS == False:
        pass
    dirs = f"./downloads/{update.from_user.id}"
    if not os.path.isdir(dirs):
        os.makedirs(dirs)
    output_filename = str(update.from_user.id)
    filename = f"./{output_filename}.zip"
    pablo = await update.reply_text("Downloading...")
    urlx = update.text.split("\n")
    rm, total, up = len(urlx), len(urlx), 0
    await pablo.edit_text(f"Total: {total}\nDownloaded: {up}\nDownloading: {rm}")
    for url in urlx:
        download_file(url, dirs)
        up += 1
        rm -= 1
        try:
            await pablo.edit_text(
                f"Total: {total}\nDownloaded: {up}\nDownloading: {rm}"
            )
        except BadRequest:
            pass
    await pablo.edit_text("Uploading...")
    if Config.AS_ZIP:
        shutil.make_archive(output_filename, "zip", dirs)
        start_time = time.time()
        await update.reply_document(
            filename,
            progress=progress_for_pyrogram,
            progress_args=("Uploading...", pablo, start_time),
        )
        await pablo.delete()
        os.remove(filename)
        shutil.rmtree(dirs)
    elif Config.AS_ZIP == False:
        dldirs = [i async for i in absolute_paths(dirs)]
        rm, total, up = len(dldirs), len(dldirs), 0
        await pablo.edit_text(f"Total: {total}\nUploaded: {up}\nUploading: {rm}")
        for files in dldirs:
            start_time = time.time()
            await update.reply_document(
                files,
                progress=progress_for_pyrogram,
                progress_args=("Uploading...", pablo, start_time),
            )
            up += 1
            rm -= 1
            try:
                await pablo.edit_text(
                    f"Total: {total}\nUploaded: {up}\nUploading: {rm}"
                )
            except BadRequest:
                pass
            time.sleep(1)
        await pablo.delete()
        shutil.rmtree(dirs)


@Client.on_message(filters.document & OWNER_FILTER)
async def loader(bot, update):
    if Config.BUTTONS:
        return await update.reply(
            "You wanna upload files as?",
            True,
            reply_markup=InlineKeyboardMarkup(CB_BUTTONS),
        )
    elif Config.BUTTONS == False:
        pass
    dirs = f"./downloads/{update.from_user.id}"
    if not os.path.isdir(dirs):
        os.makedirs(dirs)
    if not update.document.file_name.endswith(".txt"):
        return
    output_filename = update.document.file_name[:-4]
    filename = f"./{output_filename}.zip"
    pablo = await update.reply_text("Downloading...")
    fl = await update.download()
    with open(fl) as f:
        urls = f.read()
        urlx = urls.split("\n")
        rm, total, up = len(urlx), len(urlx), 0
        await pablo.edit_text(f"Total: {total}\nDownloaded: {up}\nDownloading: {rm}")
        for url in urlx:
            download_file(url, dirs)
            up += 1
            rm -= 1
            try:
                await pablo.edit_text(
                    f"Total: {total}\nDownloaded: {up}\nDownloading: {rm}"
                )
            except BadRequest:
                pass
    await pablo.edit_text("Uploading...")
    os.remove(fl)
    if Config.AS_ZIP:
        shutil.make_archive(output_filename, "zip", dirs)
        start_time = time.time()
        await update.reply_document(
            filename,
            progress=progress_for_pyrogram,
            progress_args=("Uploading...", pablo, start_time),
        )
        await pablo.delete()
        os.remove(filename)
        shutil.rmtree(dirs)
    elif Config.AS_ZIP == False:
        dldirs = [i async for i in absolute_paths(dirs)]
        rm, total, up = len(dldirs), len(dldirs), 0
        await pablo.edit_text(f"Total: {total}\nUploaded: {up}\nUploading: {rm}")
        for files in dldirs:
            start_time = time.time()
            await update.reply_document(
                files,
                progress=progress_for_pyrogram,
                progress_args=("Uploading...", pablo, start_time),
            )
            up += 1
            rm -= 1
            try:
                await pablo.edit_text(
                    f"Total: {total}\nUploaded: {up}\nUploading: {rm}"
                )
            except BadRequest:
                pass
            time.sleep(1)
        await pablo.delete()
        shutil.rmtree(dirs)


@Client.on_callback_query()
async def callbacks(bot: Client, updatex: CallbackQuery):
    cb_data = updatex.data
    update = updatex.message.reply_to_message
    await updatex.message.delete()
    dirs = f"./downloads/{update.from_user.id}"
    if not os.path.isdir(dirs):
        os.makedirs(dirs)
    if update.document:
        output_filename = update.document.file_name[:-4]
        filename = f"./{output_filename}.zip"
        pablo = await update.reply_text("Downloading...")
        fl = await update.download()
        with open(fl) as f:
            urls = f.read()
            urlx = urls.split("\n")
            rm, total, up = len(urlx), len(urlx), 0
            await pablo.edit_text(
                f"Total: {total}\nDownloaded: {up}\nDownloading: {rm}"
            )
            for url in urlx:
                download_file(url, dirs)
                up += 1
                rm -= 1
                try:
                    await pablo.edit_text(
                        f"Total: {total}\nDownloaded: {up}\nDownloading: {rm}"
                    )
                except BadRequest:
                    pass
        os.remove(fl)
    elif update.text:
        output_filename = str(update.from_user.id)
        filename = f"./{output_filename}.zip"
        pablo = await update.reply_text("Downloading...")
        urlx = update.text.split("\n")
        rm, total, up = len(urlx), len(urlx), 0
        await pablo.edit_text(f"Total: {total}\nDownloaded: {up}\nDownloading: {rm}")
        for url in urlx:
            download_file(url, dirs)
            up += 1
            rm -= 1
            try:
                await pablo.edit_text(
                    f"Total: {total}\nDownloaded: {up}\nDownloading: {rm}"
                )
            except BadRequest:
                pass
    await pablo.edit_text("Uploading...")
    if cb_data == "zip":
        shutil.make_archive(output_filename, "zip", dirs)
        start_time = time.time()
        await update.reply_document(
            filename,
            progress=progress_for_pyrogram,
            progress_args=("Uploading...", pablo, start_time),
        )
        await pablo.delete()
        os.remove(filename)
        shutil.rmtree(dirs)
    elif cb_data == "1by1":
        dldirs = [i async for i in absolute_paths(dirs)]
        rm, total, up = len(dldirs), len(dldirs), 0
        await pablo.edit_text(f"Total: {total}\nUploaded: {up}\nUploading: {rm}")
        for files in dldirs:
            start_time = time.time()
            await update.reply_document(
                files,
                progress=progress_for_pyrogram,
                progress_args=("Uploading...", pablo, start_time),
            )
            up += 1
            rm -= 1
            try:
                await pablo.edit_text(
                    f"Total: {total}\nUploaded: {up}\nUploading: {rm}"
                )
            except BadRequest:
                pass
            time.sleep(1)
        await pablo.delete()
        shutil.rmtree(dirs)
