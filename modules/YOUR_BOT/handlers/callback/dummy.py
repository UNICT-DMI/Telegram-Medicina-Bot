import telegram, logging

def dummy_callback_handler(update, context):
    bot = context.bot

    query = update.callback_query
    query_data = query.data.split(",")
    user_id = query.from_user.id

    username = query.message.chat.username
    chat_id = query.message.chat_id
    message_id = query.message.message_id

    logging.info("Handling dummy callback data from {}: {}".format(chat_id, query_data))