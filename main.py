from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters

import logging
import random
from dotenv import load_dotenv
from os import environ as env, getcwd

import config as c
from variables import *
from language_set import language, setting_lang
from database import DB



load_dotenv()
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def add_new_quote(update, context):
    pass


def full_list_quotes(update, context):
    result = DB.getFullListQuotes(update.effective_chat.id)
    context.bot.send_message(chat_id=update.effective_chat.id, text=result)

    # TO-DO:
    #       1. if list is empty, let user know about it
    #       2. make a message generator(loop to show all quotes one by one), if statement in this loop for q_owner == None

    return MAIN_MENU_HANDLER


def random_quote_handler(update, context):
    lang = language(update)
    answer = update.message.text
    
    if answer == "More":  # TO-DO: config
        return get_random_quote(update, context)
    elif answer == "Back":
        markup = ReplyKeyboardMarkup([['Get random quote', 'Full list of quotes'], ['Add a new quote']], resize_keyboard=True, one_time_keyboard=False)  # TO-DO: config
        context.bot.send_message(chat_id=update.effective_chat.id, text=c.text['start_q'][lang], reply_markup=markup)
        return MAIN_MENU_HANDLER


def get_random_quote(update, context):
    lang = language(update)
    rand_quote, q_owner = DB.getRandomQuote(update.effective_chat.id)

    context.bot.send_message(chat_id=update.effective_chat.id, text=c.text['get_random_quote'][lang])

    if rand_quote == None and q_owner == None:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, you don't have any quotes yet!") # TO-DO: config
        return MAIN_MENU_HANDLER
    else:
        markup = ReplyKeyboardMarkup([['More'], ['Back']], resize_keyboard=True, one_time_keyboard=False)  # TO-DO: config
        context.bot.send_message(chat_id=update.effective_chat.id, text=f" \"{rand_quote}\" © {q_owner}", reply_markup=markup)

        return RANDOM_QUOTE_HANDLER


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
        return ADD_NEW_QUOTE
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
            FULL_LIST_QUOTES:      [*necessary_handlers, MessageHandler(Filters.text, full_list_quotes)],
            ADD_NEW_QUOTE:         [*necessary_handlers, MessageHandler(Filters.text, add_new_quote)],
            RANDOM_QUOTE_HANDLER:  [*necessary_handlers, MessageHandler(Filters.text, random_quote_handler)],
            },

        fallbacks=[CommandHandler('stop', done)], allow_reentry=True
    )
    
    dp.add_handler(conv_handler)

    updater.start_polling()
    print('Started successfully')
    updater.idle()


if __name__ == "__main__":
    main()
