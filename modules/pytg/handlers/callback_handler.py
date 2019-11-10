import telegram, yaml, logging

from telegram.ext import CallbackQueryHandler

from modules.pytg.handlers.callback.menu import menu_callback_handler
from modules.pytg.handlers.callback.forms import forms_callback_handler

def load_callback_handlers(dispatcher):
    dispatcher.add_handler(CallbackQueryHandler(menu_callback_handler, pattern="menu,.*"))
    dispatcher.add_handler(CallbackQueryHandler(forms_callback_handler, pattern="forms,.*"))
