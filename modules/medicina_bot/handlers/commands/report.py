import telegram

def report_cmd_handler(update, context):
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
            context.bot.sendMessage(chat_id = 26349488, text = message)
            context.bot.sendMessage(chat_id = chat_id, text = "Resoconto segnalazione: \n" + " ".join(context.args) + "\n\n Grazie per la segnalazione, un rappresentante ti contatterà nel minor tempo possibile.")
        else:
            context.bot.sendMessage(chat_id = chat_id, text="⚠️ Errore ⚠️ \nInserisci la tua segnalazione dopo /report (Ad esempio /report Invasione ingegneri in corso.)")
