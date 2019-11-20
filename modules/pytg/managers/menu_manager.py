import telegram, yaml, logging

import modules.pytg.managers.text_manager as text_manager

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

cached_reply_markup = { }

def create_reply_markup(menu_id):
    # Check if reply markup is cached
    global cached_reply_markup
    if menu_id in cached_reply_markup.keys():
        return cached_reply_markup[menu_id]

    # Otherwise, create reply markup
    logging.info("Reply markup is not cached, loading...")

    menu_data = yaml.safe_load(open("menu/{}.yaml".format(menu_id), "r"))

    menu_layout = []

    # Inline menu
    if menu_data["type"] == "inline":
        for row in menu_data["markup"]:
            menu_row = []

            for button in row:
                # Retrieving callback data
                callback_data = None
                if "callback_data" in button.keys():
                    callback_data = button["callback_data"]

                # Retrieving URL
                url = None
                if "url" in button.keys():
                    url = button["url"]

                menu_row.append(
                    InlineKeyboardButton(button["text"],
                    callback_data = callback_data,
                    url = url)
                )

            menu_layout.append(menu_row)
            
        reply_markup = InlineKeyboardMarkup(menu_layout)
    else:
    # Reply menu
        for row in menu_data["markup"]:
            menu_row = []

            for button in row:
                menu_row.append(KeyboardButton(button["text"]))

            menu_layout.append(menu_row)
            
        reply_markup = ReplyKeyboardMarkup(menu_layout, resize_keyboard=True)

    if menu_data["cacheable"]:
        logging.info("Saving reply markup in cache...")
        cached_reply_markup[menu_id] = reply_markup

    return reply_markup

def switch_menu(bot, chat_id, menu_id, message_id=None):
    logging.info("Switching to menu {} for {} (message {})".format(menu_id, chat_id, message_id))

    reply_markup = create_reply_markup(menu_id)

    menu_headers = text_manager.load_menu_headers()

    if message_id:
        bot.editMessageText(
            chat_id = chat_id,
            text = menu_headers["{}".format(menu_id)],
            message_id = message_id,
            reply_markup = reply_markup
        )
    else:
        bot.sendMessage(
            chat_id = chat_id,
            text = menu_headers["{}".format(menu_id)],
            reply_markup = reply_markup
        )
