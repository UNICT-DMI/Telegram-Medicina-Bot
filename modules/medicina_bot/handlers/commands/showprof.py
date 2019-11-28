import telegram, logging
import modules.medicina_bot.managers.markdown_manager as markdown_manager

def showprof_cmd_handler(update, context):
    bot = context.bot

    message = update.message
    chat_id = message.chat.id

    username = message.from_user.username
    user_id = message.from_user.id

    bot.send_message(
        chat_id = chat_id,
        text = markdown_manager.load_markdown_document("info_prof"),
    )
