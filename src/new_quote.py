from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

import config as c
from variables import MAIN_MENU_HANDLER, NEW_QUOTE_HANDLER, ADD_Q_OWNER
from language_set import language
from database import DB


def new_quote_handler(update, context):
    lang = language(update)
    q_owner = update.message.text
    quote_text = context.chat_data['quote_text']

    context.chat_data['quote_owner'] = q_owner

    markup = ReplyKeyboardMarkup([[c.text['yes'][lang]], [c.text['no'][lang]]], resize_keyboard=True, one_time_keyboard=True)
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Here's ur quote: \"{quote_text}\" © {q_owner}. Is it correct?", reply_markup=markup)  # TO-DO: config

    DB.addNewQuote(update.effective_chat.id, quote_text, q_owner) 
    # TO-DO: 
    # 1. make a confirmation function and store in DB only after "yes". If "no", start all over again from add_new_quote()
    # 2. after adding to DB show the main menu markup and return to MAIN_MENU_HANDLER



def add_q_owner(update, context):
    lang = language(update)
    answer = update.message.text

    context.chat_data['quote_text'] = answer

    markup = ReplyKeyboardMarkup([['None']], resize_keyboard=True, one_time_keyboard=True)
    context.bot.send_message(chat_id=update.effective_chat.id, text='Type the quote owner(if no, press None): ', reply_markup=markup)  # TO-DO: config
    return NEW_QUOTE_HANDLER


def add_new_quote(update, context):
    lang = language(update)

    context.bot.send_message(chat_id=update.effective_chat.id, text='Type the quote text: ', reply_markup=ReplyKeyboardRemove())
    return ADD_Q_OWNER