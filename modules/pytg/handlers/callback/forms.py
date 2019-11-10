import telegram, logging

import modules.pytg.managers.forms_manager as forms_manager
import modules.pytg.managers.text_manager as text_manager
import modules.pytg.managers.data_manager as data_manager

def forms_callback_handler(update, context):
    bot = context.bot

    query = update.callback_query
    query_data = query.data.split(",")
    user_id = query.from_user.id

    username = query.message.chat.username
    chat_id = query.message.chat_id
    message_id = query.message.message_id

    logging.info("Handling menu callback data from {}: {}".format(chat_id, query_data))

    if query_data[1] == "fixed_reply":
        step_name = query_data[2]
        form_name = query_data[3]

        input_data = {
            "text": query_data[4],
            "action": query_data[5]
        }

        bot.editMessageReplyMarkup(
            chat_id = chat_id,
            message_id = message_id,
            reply_markup = None
        )

        forms_manager.handle_input(bot, chat_id, form_name, step_name, input_data)
        return

    if query_data[1] == "back":
        next_step_name = query_data[2]

        bot.editMessageReplyMarkup(
            chat_id = chat_id,
            message_id = message_id,
            reply_markup = None
        )

        forms_manager.set_next_step(bot, chat_id, next_step=next_step_name)
        return

    if query_data[1] == "show":
        form_name = query_data[2]

        user_data = data_manager.load_user_data(chat_id)

        forms_manager.start_form(bot, chat_id, form_name)

