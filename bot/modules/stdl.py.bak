# Copyright by X-Noid

import os, time, shutil, random, glob, asyncio, uuid, shlex, re
from typing import Tuple
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors import BadRequest, FloodWait
from motor import motor_asyncio
from bot import CMD, Config

MONGODB = os.environ['MONGO_DB_URL'] # Your Mongo DB URL

if MONGODB:
    db = motor_asyncio.AsyncIOMotorClient(MONGODB)['spotifyloader']['users']
else:
    db = ''

async def add_user(id, output_format, use_youtube, path_template):
    await db.insert_one({'id': id, 'output_format': output_format, 'use_youtube': use_youtube, 'path_template': path_template})

async def edit_stats(id, stats, stats_to_edit):
    await db.update_one({'id': id}, {'$set': {stats: stats_to_edit}})

async def is_user_exist(id):
    return True if await db.find_one({'id': id}) else False

async def get_stats(id):
    return await db.find_one({'id': id})


# Buttons
CB_BUTTONS=[
    [
        InlineKeyboardButton("Send as ZIP", callback_data="zip"),
        InlineKeyboardButton("Send one by one", callback_data="1by1"),
    ]
]

# Helpers
# https://github.com/MysteryBots/UnzipBot/blob/0bc500639ceb18492ac89c8a9de1b8d87241c3cd/UnzipBot/functions.py#L17
async def absolute_paths(directory):
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            yield os.path.abspath(os.path.join(dirpath, f))


# https://github.com/X-Gorn/FridayUB/blob/90814701558e986a68fdec2776c5aa004caa8ca5/main_startup/helper_func/basic_helpers.py#L378
async def runcmd(cmd: str) -> Tuple[str, str, int, int]:
    """ run command in terminal """
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
    
    
OWNER_FILTER = filters.incoming & filters.chat(Config.AUTH_USER)

@Client.on_message(filters.command('help') & OWNER_FILTER)
async def help(bot, update):
    if db:
        if not await is_user_exist(update.from_user.id):
            await add_user(id=update.from_user.id, output_format='mp3', use_youtube="False", path_template='{artist}/{album}/{artist} - {title}.{ext}')
    await update.reply(
        '''How to use this bot?!

Send spotify url and select the options. example regex for spotify url `https://open.spotify.com/track/5HCyWlXFPP0ywqq8TgAc0`: 
   
Commands:
- `/settings` : Settings for more features. only avalable if you've filled MONGO_DB_URL
- `/s` or `/search` : Search music and download. example: `/s Justin Bieber - Stay`
- `/help` : Show this message 
- `/start` : Show start message''', 
        True,
        reply_markup=InlineKeyboardMarkup(START_BUTTONS),
        parse_mode='markdown'
    )

@Client.on_message(filters.regex(r'http.*:[/][/]open[.]spotify[.]com.(track|album|artist|playlist)', re.M) & OWNER_FILTER)
async def downloader(bot, update):
    if db:
        if not await is_user_exist(update.from_user.id):
            await add_user(id=update.from_user.id, output_format='mp3', use_youtube="False", path_template='{artist}/{album}/{artist} - {title}.{ext}')
    await update.reply('Select Options Below!', True, reply_markup=InlineKeyboardMarkup(CB_BUTTONS))


@Client.on_message(filters.command(['search', 's']) & OWNER_FILTER)
async def search(bot, update):
    query = update.text.split(' ', 1)[1]
    rndm = uuid.uuid4().hex
    dirs = f'./{rndm}/'
    if db:
        if not await is_user_exist(update.from_user.id):
            await add_user(id=update.from_user.id, output_format='mp3', use_youtube="False", path_template='{artist}/{album}/{artist} - {title}.{ext}')
        stats = await get_stats(update.from_user.id)
        if stats['output_format']:
            of = f' --output-format {stats["output_format"]}'
        else:
            of = ''
        if bool(stats['use_youtube']):
            uy = ' --use-youtube'
        else:
            uy = ''
        if stats['path_template']:
            pt = f" --path-template '{rndm}/{stats['path_template']}'"
        else:
            pt = ''
        to_run=f"spotdl '{query}'{of}{uy}{pt}"
    else:
        to_run=f"spotdl '{query}' --path-template '{rndm}" + "/{artist}/{album}/{artist} - {title}.{ext}'"
    os.mkdir(dirs)
    await runcmd(to_run)
    art_list = os.listdir(dirs)
    dldirs = [i async for i in absolute_paths(dirs)]
    if len(dldirs) == 0:
        return await update.reply('I\'ve Found nothing.')
    x = 'all music files'
    if len(dldirs) == 1:
        x = os.path.splitext(os.path.basename(dldirs[0]))[0]
    for music in dldirs:
        try:
            await bot.send_audio(chat_id=update.from_user.id, audio=music)
        except FloodWait as e:
            await asyncio.sleep(e.x)
            await bot.send_audio(chat_id=update.from_user.id, audio=music)
    await update.reply(f'Successfully uploaded {x}', parse_mode='markdown')
    shutil.rmtree(dirs)
    

@Client.on_message(filters.command('settings') & OWNER_FILTER)
async def settings(bot, update):
    if db:
        if not await is_user_exist(update.from_user.id):
            await add_user(id=update.from_user.id, output_format='mp3', use_youtube="False", path_template='{artist}/{album}/{artist} - {title}.{ext}')
        await update.reply(
            'Select one of the settings below!',
            True,
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton('Output Format', callback_data='of'),
                ],
                [
                    InlineKeyboardButton('Use Youtube', callback_data='uy'),
                ],
                [
                    InlineKeyboardButton('Path Template', callback_data='pt'),
                ],
            ])
        )
    else:
        pass


@Client.on_callback_query()
async def callbacks(bot: Client, updatex: CallbackQuery):
    cb_data = updatex.data
    update = updatex.message.reply_to_message
    output_format_list = ['mp3', 'm4a', 'flac', 'opus', 'ogg', 'wav']
    use_youtube_list = ['True', 'False']
    if cb_data == 'of':
        stats = await get_stats(update.from_user.id)
        await updatex.message.edit(
            f'Current Output Format: `{stats["output_format"]}`\n\nSelect one of the buttons below to change your output format.',
            parse_mode='markdown'
        )
        return await updatex.message.edit_reply_markup(
            InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("MP3", callback_data="mp3"),
                    InlineKeyboardButton("M4A", callback_data="m4a"),
                ],
                [
                    InlineKeyboardButton("FLAC", callback_data="flac"),
                    InlineKeyboardButton("OPUS", callback_data="opus"),
                ],
                [
                    InlineKeyboardButton("OGG", callback_data="ogg"),
                    InlineKeyboardButton("WAV", callback_data="wav"),
                ],
                [
                    InlineKeyboardButton("Back", callback_data="back"),
                ],
            ])
        )
    if cb_data in output_format_list:
        old_stats = await get_stats(update.from_user.id)
        if old_stats['output_format'] == cb_data:
            return
        await edit_stats(id=update.from_user.id, stats='output_format', stats_to_edit=cb_data)
        stats = await get_stats(update.from_user.id)
        await updatex.message.edit(
            f'Current Output Format: `{stats["output_format"]}`\n\nSelect one of the buttons below to change your output format.',
            parse_mode='markdown'
        )
        return await updatex.message.edit_reply_markup(
            InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("MP3", callback_data="mp3"),
                    InlineKeyboardButton("M4A", callback_data="m4a"),
                ],
                [
                    InlineKeyboardButton("FLAC", callback_data="flac"),
                    InlineKeyboardButton("OPUS", callback_data="opus"),
                ],
                [
                    InlineKeyboardButton("OGG", callback_data="ogg"),
                    InlineKeyboardButton("WAV", callback_data="wav"),
                ],
                [InlineKeyboardButton("Back", callback_data="back"),],
            ])
        )
    if cb_data == 'uy':
        stats = await get_stats(update.from_user.id)
        await updatex.message.edit(
            f'Is Using Youtube: `{str(stats["use_youtube"])}`\n\nSelect one of the buttons below to change your is using youtube.',
            parse_mode='markdown'
        )
        return await updatex.message.edit_reply_markup(
            InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("True", callback_data="True"),
                    InlineKeyboardButton("False", callback_data="False"),
                ],
                [InlineKeyboardButton("Back", callback_data="back"),],
            ])
        )
    if cb_data in use_youtube_list:
        old_stats = await get_stats(update.from_user.id)
        if old_stats['use_youtube'] == cb_data:
            return
        await edit_stats(id=update.from_user.id, stats='use_youtube', stats_to_edit=cb_data)
        stats = await get_stats(update.from_user.id)
        await updatex.message.edit(
            f'Is Using Youtube: `{str(stats["use_youtube"])}`\n\nSelect one of the buttons below to change your is using youtube.',
            parse_mode='markdown'
        )
        return await updatex.message.edit_reply_markup(
            InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("True", callback_data="True"),
                    InlineKeyboardButton("False", callback_data="False"),
                ],
                [InlineKeyboardButton("Back", callback_data="back"),],
            ])
        )
    if cb_data == 'pt':
        stats = await get_stats(update.from_user.id)
        await updatex.message.edit(
            f'Current Path Template: `{str(stats["path_template"])}`\n\nSelect one of the buttons below to change your current path template.',
            parse_mode='markdown'
        )
        return await updatex.message.edit_reply_markup(
            InlineKeyboardMarkup([
                [InlineKeyboardButton("Edit Current Path Template", callback_data="edit_pt"),],
                [InlineKeyboardButton("Back", callback_data="back"),],
            ])
        )
    if cb_data == 'edit_pt':
        await updatex.message.delete()
        x = await bot.ask(
            update.from_user.id,
            'Send your custom path template.\n\nPossible values:\n{artist}\n{artists}\n{title}\n{album}\n{ext}\n{playlist}\n\nExample: `{artists}/{album}/{title} - {artist}.{ext}`\nNote: "/" is used for making new directories.',
            filters='text'
        )
        await edit_stats(id=update.from_user.id, stats='path_template', stats_to_edit=x.text)
        stats = await get_stats(update.from_user.id)
        return await update.reply(
            f'Current Path Template: `{str(stats["path_template"])}`\n\nSelect one of the buttons below to change your current path template.',
            True,
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("Edit Current Path Template", callback_data="edit_pt"),
                ],
                [
                    InlineKeyboardButton("Back", callback_data="back"),
                ],
            ]),
            parse_mode='markdown'
        )
    if cb_data == 'back':
        await updatex.message.edit(
            'Select one of the settings below!'
        )
        return await updatex.message.edit_reply_markup(
            InlineKeyboardMarkup([
                [
                    InlineKeyboardButton('Output Format', callback_data='of'),
                ],
                [
                    InlineKeyboardButton('Use Youtube', callback_data='uy'),
                ],
                [
                    InlineKeyboardButton('Path Template', callback_data='pt'),
                ],
            ])
        )
    await updatex.message.delete()
    url = updatex.message.reply_to_message.text
    rndm = uuid.uuid4().hex
    dirs = f'./{rndm}/'
    if db:
        stats = await get_stats(update.from_user.id)
        if stats['output_format']:
            of = f' --output-format {stats["output_format"]}'
        else:
            of = ''
        if bool(stats['use_youtube']):
            uy = ' --use-youtube'
        else:
            uy = ''
        if stats['path_template']:
            pt = f" --path-template '{rndm}/{stats['path_template']}'"
        else:
            pt = ''
        to_run=f"spotdl {url}{of}{uy}{pt}"
    else:
        to_run=f"spotdl {url} --path-template '{rndm}" + "/{artist}/{album}/{artist} - {title}.{ext}'"
    os.mkdir(dirs)
    xx = re.findall(r'(track|album|artist|playlist)', url, re.M)[0].capitalize()
    await runcmd(to_run)
    art_list = os.listdir(dirs)
    if cb_data == 'zip':
        x = 'zipped music files'
        dldirs = [i async for i in absolute_paths(dirs)]
        if len(dldirs) == 0:
            return await update.reply('Looks like you\'ve send wrong spotify url.')
        if len(dldirs) == 1:
            x = os.path.splitext(os.path.basename(dldirs[0]))[0]
        for artist in art_list:
            shutil.make_archive(dirs+'/'+artist, 'zip', dirs+'/'+artist)
            await update.reply_document(dirs+'/'+artist+'.zip')
    elif cb_data == '1by1':
        x = 'all music files'
        dldirs = [i async for i in absolute_paths(dirs)]
        if len(dldirs) == 0:
            return await update.reply('Looks like you\'ve send wrong spotify url.')
        if len(dldirs) == 1:
            x = os.path.splitext(os.path.basename(dldirs[0]))[0]
        for music in dldirs:
            try:
                await bot.send_audio(chat_id=update.from_user.id, audio=music)
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await bot.send_audio(chat_id=update.from_user.id, audio=music)
    await update.reply(f'Successfully uploaded {x} from a Spotify {xx} [ㅤ]({url})', parse_mode='markdown')
    shutil.rmtree(dirs)
