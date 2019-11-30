# -*- coding: utf-8 -*-

import telegram
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import CallbackContext

def printMenu(update: Update, context: CallbackContext, message):
    kb = [
      [
        # KeyboardButton('👨‍🏫 Info Prof'),
        KeyboardButton('❔ Help')
      ],
      # [ KeyboardButton('📬 Invia una segnalazione') ]
    ]
    kb_markup = ReplyKeyboardMarkup(kb, resize_keyboard=True)

    context.bot.send_message(
      chat_id=update.message.chat_id,
      text=message,
      parse_mode = telegram.ParseMode.MARKDOWN,
      reply_markup=kb_markup
    )
