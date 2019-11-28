import telegram
import modules.medicina_bot.managers.markdown_manager as markdown_manager
from telegram import Update
from telegram.ext import CallbackContext

def report_cmd_handler(update: Update, context: CallbackContext):
    bot = context.bot
    chat_id = update.message.chat.id    

    chat_username = update.message.from_user.username

    if chat_id < 0:
        context.bot.sendMessage(chat_id=chat_id, text="! La funzione /report non è ammessa nei gruppi")
    elif not chat_username:
        context.bot.sendMessage(chat_id=chat_id, text="La funzione /report non è ammessa se non si dispone di un username, aggiungi un username al tuo profilo tramite le Impostazioni di Telegram")
    else:
        if context.args:
            message = "⚠️Segnalazione⚠️ da @" + chat_username + "\n"  + " ".join(context.args)
            context.bot.sendMessage(chat_id = -315510024, text = message)
            context.bot.sendMessage(chat_id = chat_id, text = "Resoconto segnalazione: \n" + " ".join(context.args) + "\n\n Grazie per la segnalazione, un rappresentante ti contatterà nel minor tempo possibile.")
        else:
            context.bot.sendMessage(chat_id = chat_id, text="⚠️ Errore ⚠️ \nInserisci la tua segnalazione dopo /report (Ad esempio /report Invasione ingegneri in corso.)")

def report(update: Update, context: CallbackContext):
    bot = context.bot

    message = update.message
    chat_id = message.chat.id

    username = message.from_user.username
    user_id = message.from_user.id

    bot.send_message(
        chat_id = chat_id,
        text = markdown_manager.load_markdown_document("report"),
    )
