import telegram, logging, os, datetime

import modules.pytg.managers.data_manager as data_manager
import modules.pytg.managers.config_manager as config_manager

def dummy_job(context):
    logging.info("Running dummy job...")