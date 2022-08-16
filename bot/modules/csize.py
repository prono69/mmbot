# https://huzunluartemis.github.io/ChatSizeBot/

import math
import re
import time
from pyrogram.types.messages_and_media.message import Message
from pyrogram.types import Chat
from bot import LOGGER, botStartTime, Config
from bot.helpers.auth_user_check import AuthUserCheck
from pyrogram import Client, filters
from pyrogram.enums.parse_mode import ParseMode
from pyrogram.enums import ChatType
from pyrogram.errors import FloodWait
from bot.helpers.humanfuncs import TimeFormatter, get_progressbar, humanbytes
from pyrogram.errors.exceptions.bad_request_400 import \
    ChannelInvalid, ChatAdminRequired, UsernameInvalid, UsernameNotModified
from pyrogram.errors.exceptions.not_acceptable_406 import ChannelPrivate

quee = []
tg_link_regex = "(https://)?(t\.me/|telegram\.me/|telegram\.dog/)(c/)?(\d+|[a-zA-Z_0-9]+)/(\d+)$"

async def run_task(gelen: Message, duzenlenecek: Message):
    try:
        if gelen.text:
            regex = re.compile(tg_link_regex)
            match = regex.match(gelen.text)
            if not match:
                await duzenlenecek.edit_text(
                    '🇬🇧 Forward the last message on the channel or send the last message link.' \
                    '\nExample: `https://t.me/c/6262626/24234234`'
                    , disable_web_page_preview=True
                )
                return on_task_complete()
            chat_id = match.group(4)
            last_msg_id = int(match.group(5))
            if chat_id.isnumeric():
                chat_id = int(("-100" + chat_id))
        elif gelen.forward_from_chat.type in [ChatType.CHANNEL, ChatType.GROUP, ChatType.SUPERGROUP]:
            last_msg_id = gelen.forward_from_message_id
            chat_id = gelen.forward_from_chat.username or gelen.forward_from_chat.id
        else:
            await duzenlenecek.edit_text(
                    '🇬🇧 Must be a channel or group.'
                    , disable_web_page_preview=True
                )
            return on_task_complete()
        # get access to chat
        try:
            gotchat:Chat = duzenlenecek._client.get_chat(chat_id)
        except (ChannelInvalid, ChannelPrivate, ChatAdminRequired):
            duzenlenecek.edit_text('🇬🇧 You must add me to your channel/group as admin.', disable_web_page_preview=True)
            return on_task_complete()
        except (UsernameInvalid, UsernameNotModified):
            duzenlenecek.edit_text('Geçersiz kullanıcı adı.', disable_web_page_preview=True)
            return on_task_complete()
        except Exception as e:
            LOGGER.exception(e)
            duzenlenecek.edit_text(f'Errors - {e}', disable_web_page_preview=True)
            
        if not gotchat:
            duzenlenecek.edit_text('🇬🇧 You must add me to your channel/group as admin.', disable_web_page_preview=True)
            return on_task_complete()
        infochat = f"💚 **Chat Info:**" \
                f"\n\nName: `{gotchat.title}`" \
                f"\nUsername: @{gotchat.username}" \
                f"\nChat ID: `{gotchat.id}`" \
                f"\nChat DC: `{gotchat.dc_id}`" \
                f'\nFirst Message ID: `1`' \
                f'\nLast Message ID: `{last_msg_id}`'
        #
        txt = ""
        total = last_msg_id + 1
        current = 1
        empty = nomessage = nomedia = mediawosize = total_calculated_size = 0
        start_time = time.time()
        while current < total:
            current = current + 1
            # hız
            try: hiz = (current / ((time.time() - start_time).__round__())).__round__()
            except: hiz = 0
            # guncelle
            if current % 30 == 0:
                try:
                    txt = f"**% {'{:.3f}'.format(current * 100 / total)}** {get_progressbar(current, total)}" \
                        f"\n\n{infochat}\n\n💜 **Process:**" \
                        f"\n\nCalculated Total Size: `{humanbytes(total_calculated_size)}` (`{str(total_calculated_size)} bytes`)" \
                        f"\nProcessed Messages: `{current}`" \
                        f"\nTo Be Processed: `{total - current}`" \
                        f"\nDeleted Messages: `{empty}`" \
                        f"\nDamaged Messages: `{nomessage}`" \
                        f"\nNon-media Messages: `{nomedia}`" \
                        f"\nNo Filesize Medias: `{mediawosize}`" \
                        f"\nPassed Time: `{TimeFormatter(time.time() - start_time)}`" \
                        f"\nElapsed Time: `{TimeFormatter((total - current) / hiz)}`" \
                        f"\nPercent: `% {'{:.7f}'.format((current * 100 / total))}`" \
                        f"\nSpeed: `{hiz} message/sec`" \
                        f'\nBot Uptime: `{TimeFormatter(time.time() - botStartTime)}`'
                    duzenlenecek.edit_text(text=txt, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
                except: pass
            # kaydet
            message:Message = None
            try:
                message = duzenlenecek._client.get_messages(chat_id=chat_id, message_ids=current, replies=0)
            except FloodWait as e:
                time.sleep(e.value)
                message = duzenlenecek._client.get_messages(chat_id=chat_id, message_ids=current, replies=0)
            except Exception as e:
                LOGGER.exception(e)
                continue
            if not message:
                nomessage  += 1
                continue
            elif message.empty:
                empty = empty + 1
                continue
            #◙ find media
            media = None
            media_array = [message.document, message.video, message.audio, message.photo, message.animation, message.voice, message.video_note]
            for i in media_array:
                if i is not None:
                    media = i
                    break
            if not media:
                nomedia += 1
                continue
            # find size
            if media.file_size:
                total_calculated_size += int(media.file_size)
                continue
            else:
                mediawosize  += 1
                continue
        #
        if last_msg_id <= 30:
            txt = f"**% {'{:.3f}'.format(current * 100 / total)}** {get_progressbar(current, total)}" \
                f"\n\n{infochat}\n\n💜 **Process:**" \
                f"\n\nCalculated Total Size: `{humanbytes(total_calculated_size)}` (`{str(total_calculated_size)} bytes`)" \
                f"\nProcessed Messages: `{current}`" \
                f"\nDeleted Messages: `{empty}`" \
                f"\nDamaged Messages: `{nomessage}`" \
                f"\nNon-media Messages: `{nomedia}`" \
                f"\nNo Filesize Medias: `{mediawosize}`" \
                f"\nPassed Time: `{TimeFormatter(time.time() - start_time)}`" \
                f'\nBot Uptime: `{TimeFormatter(time.time() - botStartTime)}`'
        duzenlenecek.edit_text(
            f"{txt}\n\n✅ **Finished**",
            parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True
        )
    except Exception as e:
        duzenlenecek.edit_text("Cannot completed. Try again later.")
        LOGGER.exception(e)
    on_task_complete()

def on_task_complete():
    if len(quee) > 0:
        del quee[0]
    if len(quee) > 0:
        time.sleep(10)
        run_task(quee[0][0], quee[0][1])

@Client.on_message((filters.forwarded | ((filters.regex(tg_link_regex)) & filters.text)) & filters.private & filters.incoming)
def handler(_, message: Message):
    if not AuthUserCheck(message): return
    # add to quee
    duz:Message = message.reply_text(f"✅ Your Turn: {len(quee)+1}\nWait. Dont spam with same ID.", quote=True, disable_web_page_preview=True)
    quee.append([message, duz])
    if len(quee) == 1: run_task(message, duz)

@Client.on_message(filters.command(["yardım", "yardim", "h", "y"]))
def welcome(_, message: Message):
    if not AuthUserCheck(message): return
    te ="🇬🇧 Hi. Send a channel/group id and I will calculate the full size of all files." \
        "\nClick the last message in the channel / group, copy the message link, paste it to me."
    message.reply_text(te, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
