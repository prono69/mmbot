import asyncio
import io
import json
import os
import sys
import traceback
from getpass import getuser

from pyrogram import Client, filters
from pyrogram.types import ForceReply

from bot import AUTH_USER, CMD, Config
from bot.modules.markups import base_markup, refresh_space
from bot.welpers.utilities.functions import get_server_details, ip
from bot.welpers.utilities.terminal import Terminal


@Client.on_message(filters.command(CMD.TEML) & filters.user(AUTH_USER))
async def teml(bot, update):
    cmd = update.text.split(" ", 1)
    if len(cmd) == 1:
        await update.reply_text("No command to execute was given.")
        return
    cmd = cmd[1]
    try:
        t_obj = await Terminal.execute(cmd)
    except Exception as t_e:
        await update.reply(f"**ERROR:** `{t_e}`")
        return
    curruser = getuser()
    try:
        uid = os.geteuid()
    except ImportError:
        uid = 1
    output = f"`{curruser}:~#` `{cmd}`\n" if uid == 0 else f"`{curruser}:~$` `{cmd}`\n"
    count = 0
    k = None
    while not t_obj.finished:
        count += 1
        await asyncio.sleep(0.5)
        if count >= 5:
            count = 0
            out_data = f"{output}`{t_obj.read_line}`"
            try:
                if not k:
                    k = await update.reply(out_data)
                else:
                    await k.edit(out_data)
            except BaseException:
                pass
    out_data = f"`{output}{t_obj.get_output}`"
    if len(out_data) > 4096:
        if k:
            await k.delete()
        with open("terminal.txt", "w+") as ef:
            ef.write(out_data)
            ef.close()
        await update.reply_document("terminal.txt", caption=cmd)
        os.remove("terminal.txt")
        return
    send = k.edit if k else update.reply
    await send(out_data)


@Client.on_message(filters.command(CMD.RUNF) & filters.user(AUTH_USER))
async def eval(bot, update):
    status_m = await update.reply_text("`Processing...`")
    cmd = update.text.split(" ", 1)
    if len(cmd) == 1:
        await update.reply_text("No command to execute was given.")
        return
    cmd = cmd[1]

    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None

    try:
        value = await aexec(cmd, bot, update)
    except Exception:
        exc = traceback.format_exc().strip()

    stdout = redirected_output.getvalue().strip()
    stderr = redirected_error.getvalue().strip()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    output = exc or stderr or stdout or value

    if output is None:
        output = "😴"
    elif output == "":
        output = '""'
    elif isinstance(output, (dict, list)):
        try:
            output = json.dumps(output, indent=4, ensure_ascii=False)
        except Exception:
            pass

    final_output = (
        "<b>EVAL</b>: <code>{}</code>\n\n<b>OUTPUT</b>:\n<code>{}</code> \n".format(
            cmd, output
        )
    )

    if len(final_output) > Config.MAX_MESSAGE_LENGTH:
        OUTPUT = clear_string(OUTPUT)
        with BytesIO(str.encode(OUTPUT)) as f:
            f.name = "eval.txt"
            await update.reply_document(
                document=f,
                caption=f"<code>{cmd}</code>",
            )
        await status_m.delete()
    else:
        await status_m.edit(final_output)
    await update.delete()
    return


async def aexec(code, bot, update):
    exec(
        f"async def __aexec(bot, update): "
        + "".join(f"\n {l}" for l in code.split("\n"))
    )
    return await locals()["__aexec"](bot, update)


@Client.on_message(filters.command(CMD.CD) & filters.user(AUTH_USER))
async def cd(bot, update):
    chdir = await bot.ask(
        update.chat.id,
        "please enter the folder path that you want?",
        timeout=120,
        filters=filters.reply,
        reply_markup=ForceReply(),
    )
    try:
        os.chdir(chdir.text)
        await update.reply_text(f"Changed Directory to `{os.getcwd()}`")
    except FileNotFoundError:
        await update.reply_text("incorrect path!")
    except TimeoutError:
        pass
    except Exception as e:
        await update.reply_text(str(e))


@Client.on_message(filters.command(CMD.FILES) & filters.user(AUTH_USER))
async def my_files(bot, update):
    await update.reply_text("what you want to show?", reply_markup=base_markup)


@Client.on_message(filters.command(CMD.IP) & filters.user(AUTH_USER))
async def ip_cmd(bot, update):
    await update.reply(ip(), parse_mode="markdown")


@Client.on_message(filters.command(CMD.STATUS) & filters.user(AUTH_USER))
async def stats(bot, update):
    await update.reply_text(get_server_details(), reply_markup=refresh_space)
