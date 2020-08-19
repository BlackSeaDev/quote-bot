from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters

import logging
from dotenv import load_dotenv
from os import environ as env, getcwd

import config as c
from variables import *
from language_set import language, setting_lang
from database import DB

from random_quote import get_random_quote, random_quote_handler
from all_quotes import full_list_quotes
from new_quote import add_new_quote, add_q_owner, new_quote_handler

### Bot's logic starts from the BOTTOM
### If you see any errors connected with uppercase variables(i.e. NEW_QUOTE_HANDLER) and importing, DON'T pay attention to them

load_dotenv()
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def unknown_command(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Unknown command')
    filename = getcwd() + '/media/photo.png'
    with open(filename, 'rb') as file:
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=file, caption='Press this button and choose the option') #TO-DO: config


def main_menu(update, context):
    answer = update.message.text

    if answer == 'Get random quote':  # TO-DO: config
        return get_random_quote(update, context)
    elif answer == 'Full list of quotes':
        return full_list_quotes(update, context)
    elif answer == 'Add a new quote':
        return add_new_quote(update, context)
    else:
        return unknown_command(update, context)


def start(update, context):
    lang = language(update)
    
    if lang == 0 or lang == 1:
        markup = ReplyKeyboardMarkup([['Get random quote', 'Full list of quotes'], ['Add a new quote']], resize_keyboard=True, one_time_keyboard=False)  # TO-DO: config
        #update.message.reply_text(text='HErsae2', reply_markup=markup)
        context.bot.send_message(chat_id=update.effective_chat.id, text=c.text['start_q'][lang], reply_markup=markup)
    else:
        return LANG

    return MAIN_MENU_HANDLER


def done(update, context):
    pass


def main():
    print('Starting...')
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
            GET_RANDOM_QUOTE:      [*necessary_handlers, MessageHandler(Filters.text, get_random_quote)],
            RANDOM_QUOTE_HANDLER:  [*necessary_handlers, MessageHandler(Filters.text, random_quote_handler)],
            FULL_LIST_QUOTES:      [*necessary_handlers, MessageHandler(Filters.text, full_list_quotes)],
            ADD_NEW_QUOTE:         [*necessary_handlers, MessageHandler(Filters.text, add_new_quote)],
            ADD_Q_OWNER:           [*necessary_handlers, MessageHandler(Filters.text, add_q_owner)],
            NEW_QUOTE_HANDLER:     [*necessary_handlers, MessageHandler(Filters.text, new_quote_handler)],
            },

        fallbacks=[CommandHandler('stop', done)], allow_reentry=True
    )
    
    dp.add_handler(conv_handler)

    updater.start_polling()
    print('Started successfully')
    updater.idle()


if __name__ == "__main__":
    main()
