import telegram, logging

import modules.pytg.managers.text_manager as text_manager

def start_cmd_handler(update, context):
    bot = context.bot

    message = update.message
    chat_id = message.chat.id

    username = message.from_user.username
    user_id = message.from_user.id

    logging.info("Received start command update from {} ({}) in chat {}".format(username, user_id, chat_id))
    
    phrases = text_manager.load_phrases()

    bot.sendMessage(
        chat_id = chat_id,
        text = phrases["hello_world"]
    )
