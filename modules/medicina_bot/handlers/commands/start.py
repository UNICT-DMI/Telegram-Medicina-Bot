import telegram
from modules.medicina_bot.utils.keyboard_menu import printMenu

import modules.medicina_bot.managers.markdown_manager as markdown_manager

def start_cmd_handler(update, context):
    bot = context.bot
    chat_id = update.message.chat.id    
    text = markdown_manager.load_markdown_document("start")

    printMenu(update, context, text)
