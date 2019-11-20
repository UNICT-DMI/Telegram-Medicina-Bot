import telegram, logging

import modules.pytg.managers.menu_manager as menu_manager
import modules.pytg.managers.text_manager as text_manager

def help_cmd_handler(update, context):
    bot = context.bot

    message = update.message
    chat_id = message.chat.id

    username = message.from_user.username
    user_id = message.from_user.id

    menu_headers = text_manager.load_menu_headers()

    bot.send_message(
        chat_id = chat_id,
        text = menu_headers["help"],
        reply_markup = menu_manager.create_reply_markup("help")
    )
