import telegram, yaml, logging

import modules.pytg.managers.menu_manager as menu_manager
import modules.pytg.managers.text_manager as text_manager

def menu_callback_handler(update, context):
    bot = context.bot

    query = update.callback_query
    query_data = query.data.split(",")
    user_id = query.from_user.id

    username = query.message.chat.username
    chat_id = query.message.chat_id
    message_id = query.message.message_id

    logging.info("Handling menu callback data from {}: {}".format(chat_id, query_data))

    if query_data[1] == "switch":
        menu_id = query_data[2]

        menu_manager.switch_menu(bot, chat_id, menu_id, message_id)
