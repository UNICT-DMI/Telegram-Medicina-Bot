import telegram, logging

import modules.pytg.managers.data_manager as data_manager
import modules.pytg.managers.forms_manager as forms_manager
import modules.pytg.managers.text_manager as text_manager

from telegram.ext import MessageHandler, Filters 

def load_messages_handlers(dispatcher):
    dispatcher.add_handler(MessageHandler(Filters.text, text_message_handler))
    dispatcher.add_handler(MessageHandler(Filters.photo, photo_message_handler))
    pass

def text_message_handler(update, context):
    bot = context.bot

    message = update.message

    if not message or not message.chat:
        return

    chat_id = message.chat.id

    username = message.from_user.username
    user_id = message.from_user.id

    text = message.text

    logging.info("Received text message update from {} ({}) in chat {}: {}".format(username, user_id, chat_id, text))

    if not data_manager.has_user_data(chat_id):
        return

    # Check if the bot is waiting for a form input 
    user_data = data_manager.load_user_data(chat_id)

    current_user_form_id = user_data["current_form"]

    if current_user_form_id:
        form_data = data_manager.load_form_data(current_user_form_id)
        form_name = form_data["form_name"]
        form_steps = text_manager.load_form_steps(form_name)

        step_data = form_steps[form_data["current_step"]]

        print(step_data)

        if step_data["type"] == "text_field":
            input_data = {
                "text": text
            }
        elif step_data["type"] == "image_field":
            if not message.photo:
                return 

            photos = message.photo
            print(photos)

            input_data = {
                "image_url": None 
            }
        else:
            return

        forms_manager.handle_input(bot, chat_id, form_name, form_data["current_step"], input_data)

def photo_message_handler(update, context):
    bot = context.bot

    message = update.message

    if not message or not message.chat or not message.photo:
        return

    chat_id = message.chat.id

    username = message.from_user.username
    user_id = message.from_user.id

    logging.info("Received photo message update from {} ({}) in chat {}".format(username, user_id, chat_id))

    if not data_manager.has_user_data(chat_id):
        return

    # Check if the bot is waiting for a form input 
    user_data = data_manager.load_user_data(chat_id)

    current_user_form_id = user_data["current_form"]

    if current_user_form_id:
        form_data = data_manager.load_form_data(current_user_form_id)
        form_name = form_data["form_name"]
        form_steps = text_manager.load_form_steps(form_name)

        step_data = form_steps[form_data["current_step"]]

        if step_data["type"] != "image_field":
            return

        photos = message.photo
        image_id = photos[-1].file_id
        image_url = bot.getFile(image_id).file_path

        input_data = {
            "image_id": image_id,
            "image_url": image_url 
        }

        forms_manager.handle_input(bot, chat_id, form_name, form_data["current_step"], input_data)




