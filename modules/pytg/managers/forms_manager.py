import telegram, yaml, logging, traceback

import modules.pytg.managers.data_manager as data_manager
import modules.pytg.managers.image_manager as image_manager
import modules.pytg.managers.text_manager as text_manager

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

digesters = {}

def add_digester(key, func):
    digesters[key] = func

def clear_user_form_data(bot, chat_id, delete_messages=True):
    logging.info("Clearing form data for user {}".format(chat_id))

    user_data = data_manager.load_user_data(chat_id)

    if user_data["current_form"]:
        form_id = user_data["current_form"]
        # Clear form messages
        form_data = data_manager.load_form_data(form_id)
        
        if (not form_data["digested"]) and delete_messages:
            for form_message_id in form_data["messages"]:
                try:
                    bot.deleteMessage(
                        chat_id = chat_id,
                        message_id = form_message_id
                    )
                except:
                    logging.info("Unable to delete message {}".format(form_message_id))

        # Update user data
        data_manager.delete_form_data(form_id)
        user_data["current_form"] = None
        data_manager.save_user_data(chat_id, user_data)

def start_form(bot, chat_id, form_name):
    logging.info("Starting form {} for {}".format(form_name, chat_id))

    # Update user data
    clear_user_form_data(bot, chat_id)

    user_data = data_manager.load_user_data(chat_id)

    form_id = "{}_{}".format(chat_id, form_name)
    data_manager.create_form_data(form_id)

    user_data["current_form"] = form_id

    data_manager.save_user_data(chat_id, user_data)

    # Show form to user
    steps = text_manager.load_form_steps(form_name)

    first_step = steps["meta"]["first_step"]

    form_data = data_manager.load_form_data(form_id)

    form_data["form_name"] = form_name
    form_data["current_step"] = first_step

    data_manager.save_form_data(form_id, form_data)
    show_current_step(bot, chat_id)

def set_next_step(bot, chat_id, form_id=None, next_step=None):
    if form_id == None:
        user_data = data_manager.load_user_data(chat_id)
        form_id = user_data["current_form"]

    form_data = data_manager.load_form_data(form_id)
    form_name = form_data["form_name"]
    form_steps = text_manager.load_form_steps(form_name)

    current_step_data = form_steps[form_data["current_step"]]

    if next_step == None:
        next_step = current_step_data["next_step"]

    logging.info("Showing next step to {} ({} {})".format(chat_id, form_id, next_step))

    if next_step:
        if next_step == "_RESET":
            clear_user_form_data(bot, chat_id, False)
            return 

        form_data["current_step"] = next_step
        data_manager.save_form_data(form_id, form_data)
        show_current_step(bot, chat_id)
    else:
        digest_form(bot, chat_id, form_id)

def digest_form(bot, chat_id, form_id):
    logging.info("Digesting form {} for {}".format(form_id, chat_id))

    # Load user data
    user_data = data_manager.load_user_data(chat_id)

    # Digest the form
    form_data = data_manager.load_form_data(form_id)
    form_name = form_data["form_name"]

    global digesters
    digester = digesters[form_name]
    digester(bot, form_data["form_entries"], user_data)

    # Update form flag
    form_data["digested"] = True
    data_manager.save_form_data(form_id, form_data)

    # Clear user form data
    # clear_user_form_data(bot, chat_id)

def format_step_text(step_text, form_entries):
    for key in form_entries.keys():
        key_expression = "${}$".format(key)
        step_text = step_text.replace(key_expression, form_entries[key])

    return step_text

def append_back_button(menu_layout, previous_step):
    phrases = text_manager.load_phrases()

    menu_layout.append([InlineKeyboardButton(phrases["back"], callback_data="forms,back,{}".format(previous_step))])

def show_current_step(bot, chat_id):
    user_data = data_manager.load_user_data(chat_id)

    form_id = user_data["current_form"]

    form_data = data_manager.load_form_data(form_id)
    form_name = form_data["form_name"]
    form_steps = text_manager.load_form_steps(form_name)

    step_name = form_data["current_step"]
    current_step_data = form_steps[step_name]

    # Message 
    if current_step_data["type"] == "message":
        step_text = current_step_data["text"]

        if "format" in current_step_data.keys() and current_step_data["format"]:
            form_entries = form_data["form_entries"]
            step_text = format_step_text(step_text, form_entries)

        reply_markup = None

        # Check if the step requires a back button
        if "previous_step" in current_step_data.keys():
            menu_layout = []
            append_back_button(menu_layout, current_step_data["previous_step"])
            reply_markup = InlineKeyboardMarkup(menu_layout)

        sent_message = bot.sendMessage(
            chat_id=chat_id,
            text=step_text,
            parse_mode=telegram.ParseMode.MARKDOWN,
            reply_markup = reply_markup
        )

        set_next_step(bot, chat_id, form_id=form_id, next_step = current_step_data["next_step"])

        # Add new message IDs
        if data_manager.has_form_data(form_id):
            form_data = data_manager.load_form_data(form_id)
            form_data["messages"].append(sent_message.message_id)
            data_manager.save_form_data(form_id, form_data)

        return

    # Text or image field
    if current_step_data["type"] == "text_field" or current_step_data["type"] == "image_field":
        step_text = current_step_data["text"]

        if "format" in current_step_data.keys() and current_step_data["format"]:
            form_entries = form_data["form_entries"]
            step_text = format_step_text(step_text, form_entries)

        reply_markup = None

        # Check if the step requires a back button
        if "previous_step" in current_step_data.keys():
            menu_layout = []
            append_back_button(menu_layout, current_step_data["previous_step"])
            reply_markup = InlineKeyboardMarkup(menu_layout)

        sent_message = bot.sendMessage(
            chat_id=chat_id,
            text=step_text,
            parse_mode=telegram.ParseMode.MARKDOWN,
            reply_markup = reply_markup
        )

        # Add new message IDs
        if data_manager.has_form_data(form_id):
            form_data = data_manager.load_form_data(form_id)
            form_data["messages"].append(sent_message.message_id)
            data_manager.save_form_data(form_id, form_data)

        return

    if current_step_data["type"] == "fixed_reply":
        # Load options
        options = current_step_data["options"]

        # Create reply markup
        menu_layout = []

        for options_row in options:
            row = []

            for option in options_row:
                action = ""

                if "action" in option.keys():
                    action = option["action"]

                button_data = "forms,fixed_reply,{},{},{},{}".format(step_name, form_name, option["text"], action)

                row.append(InlineKeyboardButton(option["text"], callback_data=button_data))

            menu_layout.append(row)

        if "previous_step" in current_step_data.keys():
            append_back_button(menu_layout, current_step_data["previous_step"])

        menu_markup = InlineKeyboardMarkup(menu_layout)

        # Format step text (if necessary)
        step_text = current_step_data["text"]

        if "format" in current_step_data.keys() and current_step_data["format"]:
            form_entries = form_data["form_entries"]
            step_text = format_step_text(step_text, form_entries)

        # Send message
        sent_message = bot.sendMessage(
            chat_id=chat_id,
            text=step_text,
            parse_mode=telegram.ParseMode.MARKDOWN,
            reply_markup=menu_markup
        )

        # Add new message IDs
        if data_manager.has_form_data(form_id):
            form_data = data_manager.load_form_data(form_id)
            form_data["messages"].append(sent_message.message_id)
            data_manager.save_form_data(form_id, form_data)

def handle_input(bot, chat_id, form_name, step_name, input_data):
    logging.info("Handling input of {} on form {} (step name = {}, input data = {})".format(chat_id, form_name, step_name, input_data))

    # Check if it's an action input
    if "action" in input_data.keys() and len(input_data["action"]) > 0:
        actions = input_data["action"].split(";")

        if actions[0] == "jump":
            next_step_name = actions[1]
            set_next_step(bot, chat_id, next_step=next_step_name)
            return

    # TODO: Implement input handling for each form (if any)

    form_steps = text_manager.load_form_steps(form_name)
    step_data = form_steps[step_name]

    if "output" in step_data.keys():
        if step_data["type"] == "text_field":
            step_output = input_data["text"]
        elif step_data["type"] == "image_field":
            image_manager.download_image(input_data["image_id"], input_data["image_url"])

            step_output = input_data["image_id"]

        user_data = data_manager.load_user_data(chat_id)

        current_user_form_id = user_data["current_form"]
        form_data = data_manager.load_form_data(current_user_form_id)
        form_data["form_entries"][step_data["output"]] = step_output
        data_manager.save_form_data(current_user_form_id, form_data)

        set_next_step(bot, chat_id, form_id=current_user_form_id)

        return

    logging.info("WARNING: Unable to handle this input.")
