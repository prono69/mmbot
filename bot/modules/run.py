import smtplib, ssl, os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot import CMD, Config

# Environment Variables


@Client.on_message(filters.command(CMD.EMAIL) & filters.chat(Config.AUTH_USER))
async def email_sender(bot, update):
    if update.text == '/email':
        await update.reply('Example: `/email receiver-email@gmail.com`')
        return
    receiver = update.text.split(' ', 1)[1]
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    subject = await bot.ask(update.chat.id, 'Send Your Subject', filters='text', timeout=300)
    message = await bot.ask(update.chat.id, 'Send Your Message', filters='text', timeout=300)
    text = f'Subject: {subject.text}\n\n{message.text}'
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(Config.SENDER, Config.PASSWORD)
        server.sendmail(Config.SENDER, receiver, text)
    await update.reply('Successfully Sended to Receiver/Target.')

