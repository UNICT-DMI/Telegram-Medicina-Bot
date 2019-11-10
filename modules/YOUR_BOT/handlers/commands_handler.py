import telegram, yaml, logging

from telegram.ext import CommandHandler

from modules.YOUR_BOT.handlers.commands.start import start_cmd_handler

def load_command_handlers(dispatcher):
    dispatcher.add_handler(CommandHandler("start", start_cmd_handler))

