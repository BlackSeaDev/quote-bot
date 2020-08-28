from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

import config
from variables import MAIN_MENU_HANDLER, NEW_QUOTE_HANDLER, ADD_Q_OWNER, ADD_NEW_QUOTE
from language_set import language
from database import DB


def new_quote_handler(update, context):
    answer = update.message.text
    lang = language(update)

    q_owner = update.message.text
    quote_text = context.chat_data['quote_text']
    context.chat_data['quote_owner'] = q_owner

    markup = ReplyKeyboardMarkup([[config.language_config['yes'][lang]], [config.language_config['no'][lang]]], resize_keyboard=True, one_time_keyboard=True)
    context.bot.send_message(chat_id=update.effective_chat.id, text=config.language_config['show_new_quote'][lang].format(quote_text, context.chat_data['quote_owner']), reply_markup=markup)

    if answer == config.language_config['yes'][lang]:
        DB.addNewQuote(update.effective_chat.id, quote_text, q_owner)
        context.bot.send_message(chat_id=update.effective_chat.id, text=config.language_config['adding_quote_to_database'][lang], reply_markup=markup)
        markup = ReplyKeyboardMarkup([[config.language_config['get_random_quote'][lang], config.language_config['full_list_of_quotes'][lang]], [config.language_config['add_new_quote'][lang]]], resize_keyboard=True, one_time_keyboard=False)
        context.bot.send_message(chat_id=update.effective_chat.id, text=config.language_config['start_q'][lang], reply_markup=markup)
        return MAIN_MENU_HANDLER
    elif answer == config.language_config['no'][lang]:
        context.bot.send_message(chat_id=update.effective_chat.id, text=config.language_config['type_the_quote'][lang], reply_markup=ReplyKeyboardRemove())
        return ADD_Q_OWNER

    # TO-DO: 
    # 1. make "no", start all over again from add_new_quote()


def add_q_owner(update, context):
    lang = language(update)
    answer = update.message.text

    context.chat_data['quote_text'] = answer

    markup = ReplyKeyboardMarkup([['None']], resize_keyboard=True, one_time_keyboard=True)
    context.bot.send_message(chat_id=update.effective_chat.id, text=config.language_config['type_the_quote_owner'][lang], reply_markup=markup)
    return NEW_QUOTE_HANDLER


def add_new_quote(update, context):
    lang = language(update)

    context.bot.send_message(chat_id=update.effective_chat.id, text=config.language_config['type_the_quote'][lang], reply_markup=ReplyKeyboardRemove())
    return ADD_Q_OWNER
