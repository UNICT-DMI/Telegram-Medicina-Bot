import telegram, yaml, logging

import modules.pytg.managers.forms_manager as forms_manager

from modules.YOUR_BOT.handlers.digest.dummy import dummy_digester

def load_digesters():
    forms_manager.add_digester("dummy", dummy_digester)
