import smtplib, ssl, os, pyromod.listen
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot import AUTH_USER, CMD

# Environment Variables
SENDER = os.environ['EMAIL'] # Sender Email/Your Email
PASSWORD = os.environ['PASSWORD'] # Your Email's Password


@Client.on_message(filters.command('send') & filters.chat(AUTH_USER))
async def email_sender(bot, update):
    if update.text == '/send':
        await update.reply('Example: `/send receiver-email@gmail.com`')
        return
    receiver = update.text.split(' ', 1)[1]
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    subject = await bot.ask(update.chat.id, 'Send Your Subject', filters='text', timeout=300)
    message = await bot.ask(update.chat.id, 'Send Your Message', filters='text', timeout=300)
    text = f'Subject: {subject.text}\n\n{message.text}'
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(SENDER, PASSWORD)
        server.sendmail(SENDER, receiver, text)
    await update.reply('Successfully Sended to Receiver/Target.')

