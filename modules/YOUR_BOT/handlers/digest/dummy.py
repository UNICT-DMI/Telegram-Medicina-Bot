import logging, datetime

import modules.pytg.managers.data_manager as data_manager
import modules.pytg.managers.config_manager as config_manager

def dummy_digester(bot, form_entries, user_data):
    logging.info("Dummy digesting ({}, {})".format(user_data["chat_id"], form_entries))

