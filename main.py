from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters

import logging
import random
from dotenv import load_dotenv
from os import environ as env

import config as c
from variables import *
from language_set import language, setting_lang



load_dotenv()
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def main_menu(update, context):
    answer = update.message.text

    if answer == 'Huy':
        # return GET_RANDOM_PHRASE
        pass

    return MAIN_MENU_HANDLER


def get_random_phrase(upadte, context):
    markup = ReplyKeyboardMarkup([['Herase', 'Fuck bot api'], ['Huyase']], resize_keyboard=True, one_time_keyboard=False)
    context.bot.send_message(chat_id=update.effective_chat.id, text=c.text['start'][lang], reply_markup=markup)
    return MAIN_MENU_HANDLER


def start(update, context):
    lang = language(update)
    
    if lang == 0 or lang == 1:
        markup = ReplyKeyboardMarkup([['Herase', 'Fuck bot api'], ['Huyase']], resize_keyboard=True, one_time_keyboard=False)
        #update.message.reply_text(text='HErsae2', reply_markup=markup)
        context.bot.send_message(chat_id=update.effective_chat.id, text=c.text['start'][lang], reply_markup=markup)
    else:
        return LANG

    return MAIN_MENU_HANDLER


def done(update, context):
    pass


def main():
    api_key = env.get('API_KEY')
    updater = Updater(token=api_key, use_context=True)
    dp = updater.dispatcher


    necessary_handlers = [CommandHandler('start', start)]
                        #   CommandHandler('stop', done),
                        #   CommandHandler('admin', admin)],


    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            LANG:                  [*necessary_handlers, MessageHandler(Filters.text, setting_lang)],
            MAIN_MENU_HANDLER:     [*necessary_handlers, MessageHandler(Filters.text, main_menu)],
            GET_RANDOM_PHRASE:     [*necessary_handlers, MessageHandler(Filters.text, get_random_phrase)],
            # ADD_PHRASE:            [*necessary_handlers, MessageHandler(Filters.text, add_phrase)],
            # GET_LIST_OF_PHRASES:   [*necessary_handlers, MessageHandler(Filters.text, get_list_of_phrase)],
            },

        fallbacks=[CommandHandler('stop', done)], allow_reentry=True
    )
    
    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
