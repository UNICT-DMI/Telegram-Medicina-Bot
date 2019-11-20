from telegram import Update
from telegram.ext import CallbackContext

def send_message(update: Update, context: CallbackContext, messaggio):
    msg = ""
    righe = messaggio.split('\n')
    for riga in righe:
        if riga.strip() == "" and len(msg) > 3000:
            context.bot.sendMessage(chat_id=update.message.chat_id, text=msg, parse_mode='Markdown')
            msg = ""
        else:
            msg += riga + "\n"
    context.bot.sendMessage(chat_id=update.message.chat_id, text=msg, parse_mode='Markdown')
