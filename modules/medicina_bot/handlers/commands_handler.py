import telegram, yaml, logging

from telegram.ext import CommandHandler

from modules.medicina_bot.handlers.commands.start import start_cmd_handler
from modules.medicina_bot.handlers.commands.help  import help_cmd_handler
from modules.medicina_bot.handlers.commands.prof  import prof_cmd_handler
from modules.medicina_bot.handlers.commands.report  import report_cmd_handler

def load_command_handlers(dispatcher):
    dispatcher.add_handler(CommandHandler("start",   start_cmd_handler))
    dispatcher.add_handler(CommandHandler("help",    help_cmd_handler))
    dispatcher.add_handler(CommandHandler("prof",    prof_cmd_handler, pass_args=True))
    dispatcher.add_handler(CommandHandler("report",  report_cmd_handler, pass_args=True))
