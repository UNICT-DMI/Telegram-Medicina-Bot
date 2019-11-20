import telegram, logging

import modules.medicina_bot.managers.markdown_manager as markdown_manager

# Markdown messages handler
# Responsible for loading markdown texts and send them as messages when requested
def mdmsg_callback_handler(update, context):
    bot = context.bot

    query = update.callback_query
    query_data = query.data.split(",")
    user_id = query.from_user.id

    username = query.message.chat.username
    chat_id = query.message.chat_id
    message_id = query.message.message_id

    # logging.info("Handling mdmsg callback data from {}: {}".format(chat_id, query_data))

    document_id = query_data[1]

    bot.send_message(
        chat_id = chat_id,
        text = markdown_manager.load_markdown_document(document_id),
        parse_mode = telegram.ParseMode.MARKDOWN
    ) 