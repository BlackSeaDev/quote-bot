from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

import config
from variables import MAIN_MENU_HANDLER, RANDOM_QUOTE_HANDLER
from language_set import language
from database import DB


def random_quote_handler(update, context):
    lang = language(update)
    answer = update.message.text
    
    if answer == config.language_config['more'][lang]:
        return get_random_quote(update, context)
    elif answer == config.language_config['back'][lang]:
        markup = ReplyKeyboardMarkup([[config.language_config['get_random_quote'][lang], config.language_config['full_list_of_quotes'][lang]], [config.language_config['add_new_quote'][lang]]], resize_keyboard=True, one_time_keyboard=False)
        context.bot.send_message(chat_id=update.effective_chat.id, text=config.language_config['start_q'][lang], reply_markup=markup)
        return MAIN_MENU_HANDLER


def get_random_quote(update, context):
    lang = language(update)
    rand_quote, q_owner = DB.getRandomQuote(update.effective_chat.id)

    context.bot.send_message(chat_id=update.effective_chat.id, text=config.language_config['get_random_quote'][lang])

    if rand_quote is None and q_owner is None:  # TO-DO: add one more if statement: when q_owner == None, don't show this
        context.bot.send_message(chat_id=update.effective_chat.id, text=config.language_config['empty_list'][lang])
        return MAIN_MENU_HANDLER
    else:
        markup = ReplyKeyboardMarkup([[config.language_config['more'][lang]], [config.language_config['back'][lang]]], resize_keyboard=True, one_time_keyboard=False)
        context.bot.send_message(chat_id=update.effective_chat.id, text=f" \"{rand_quote}\" © {q_owner}", reply_markup=markup)

        return RANDOM_QUOTE_HANDLER
