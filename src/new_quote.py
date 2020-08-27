from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

import config as c
from variables import MAIN_MENU_HANDLER, NEW_QUOTE_HANDLER, ADD_Q_OWNER, ADD_NEW_QUOTE
from language_set import language
from database import DB


def new_quote_handler(update, context):
    answer = update.message.text
    lang = language(update)
    q_owner = update.message.text
    quote_text = context.chat_data['quote_text']
    context.chat_data['quote_owner'] = q_owner
    markup = ReplyKeyboardMarkup([[c.text['yes'][lang]], [c.text['no'][lang]]], resize_keyboard=True, one_time_keyboard=True)
    context.bot.send_message(chat_id=update.effective_chat.id, text=c.text['show_new_quote'][lang].format(quote_text, q_owner), reply_markup=markup)

    if answer == c.text['yes'][lang]:
        DB.addNewQuote(update.effective_chat.id, quote_text, q_owner)
        context.bot.send_message(chat_id=update.effective_chat.id, text=c.text['adding_quote_to_database'][lang], reply_markup=markup)
        markup = ReplyKeyboardMarkup([[c.text['get_random_quote'][lang], c.text['full_list_of_quotes'][lang]], [c.text['add_new_quote'][lang]]], resize_keyboard=True, one_time_keyboard=False)
        context.bot.send_message(chat_id=update.effective_chat.id, text=c.text['start_q'][lang], reply_markup=markup)
        return MAIN_MENU_HANDLER
    elif answer == c.text['no'][lang]:
        add_new_quote(update, context)
        return ADD_NEW_QUOTE

    # TO-DO: 
    # 1. make a confirmation function and store in DB only after "yes". If "no", start all over again from add_new_quote()
    # 2. after adding to DB show the main menu markup and return to MAIN_MENU_HANDLER


def add_q_owner(update, context):
    lang = language(update)
    answer = update.message.text

    context.chat_data['quote_text'] = answer

    markup = ReplyKeyboardMarkup([['None']], resize_keyboard=True, one_time_keyboard=True)
    context.bot.send_message(chat_id=update.effective_chat.id, text=c.text['type_the_quote_owner'][lang], reply_markup=markup)  # TO-DO: config
    return NEW_QUOTE_HANDLER


def add_new_quote(update, context):
    lang = language(update)

    context.bot.send_message(chat_id=update.effective_chat.id, text=c.text['type_the_quote'][lang], reply_markup=ReplyKeyboardRemove())
    return ADD_Q_OWNER
