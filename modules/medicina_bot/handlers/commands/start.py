import telegram

import modules.pytg.managers.text_manager as text_manager

def start_cmd_handler(update, context):
    bot = context.bot
    chat_id = update.message.chat.id    
    phrases = text_manager.load_phrases()

    bot.sendMessage(
        chat_id = chat_id,
        text = phrases["start"]
    )
