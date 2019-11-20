import telegram, logging, threading, datetime

import modules.pytg.managers.config_manager as config_manager

import modules.pytg.handlers.messages_handler as pytg_messages_handler
import modules.pytg.handlers.callback_handler as pytg_callback_handler

# Ideally, your bot should want to implements all those components
import modules.medicina_bot.handlers.callback_handler as callback_handler
import modules.medicina_bot.handlers.commands_handler as commands_handler
import modules.medicina_bot.handlers.jobs_handler as jobs_handler

from telegram.ext import Updater, MessageHandler, CommandHandler, Filters 

def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO,
        # filename="pytg-bot.log"
    )

    logging.info(" ### Launching PyTG Bot... ### ")
    logging.info(str(datetime.datetime.now()))

    settings = config_manager.load_settings_file()

    bot = telegram.Bot(settings["token"])

    updater = Updater(settings["token"], use_context=True)
    dispatcher = updater.dispatcher

    commands_handler.load_command_handlers(dispatcher)
    callback_handler.load_callback_handlers(dispatcher)

    jobs_handler.schedule_jobs(updater.job_queue)

    # PyTG boilerplate
    pytg_callback_handler.load_callback_handlers(dispatcher)
    pytg_messages_handler.load_messages_handlers(dispatcher)

    # Start polling
    updater.start_polling()
    logging.info("Polling.")

if __name__ == '__main__':
    main()
