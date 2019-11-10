import telegram, yaml, logging

from telegram.ext import CallbackQueryHandler

from modules.YOUR_BOT.handlers.callback.dummy import dummy_callback_handler

def load_callback_handlers(dispatcher):
    dispatcher.add_handler(CallbackQueryHandler(dummy_callback_handler, pattern="dummy,.*"))
