import telegram, logging, os, datetime

import modules.pytg.managers.data_manager as data_manager
import modules.pytg.managers.config_manager as config_manager

from modules.medicina_bot.utils.professors_utils import *

def scrape_professors_job(context):
    logging.info("Running scrape professors job...")

    scrape_professors()
