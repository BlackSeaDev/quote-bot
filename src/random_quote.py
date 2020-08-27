from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

import config as c
from variables import MAIN_MENU_HANDLER, RANDOM_QUOTE_HANDLER
from language_set import language
from database import DB


def random_quote_handler(update, context):
    lang = language(update)
    answer = update.message.text
    
    if answer == c.text['more'][lang]:
        return get_random_quote(update, context)
    elif answer == c.text['back'][lang]:
        markup = ReplyKeyboardMarkup([[c.text['get_random_quote'][lang], c.text['full_list_of_quotes'][lang]], [c.text['add_new_quote'][lang]]], resize_keyboard=True, one_time_keyboard=False)
        context.bot.send_message(chat_id=update.effective_chat.id, text=c.text['start_q'][lang], reply_markup=markup)
        return MAIN_MENU_HANDLER


def get_random_quote(update, context):
    lang = language(update)
    rand_quote, q_owner = DB.getRandomQuote(update.effective_chat.id)

    context.bot.send_message(chat_id=update.effective_chat.id, text=c.text['get_random_quote'][lang])

    if rand_quote is None and q_owner is None:  # TO-DO: add one more if statement: when q_owner == None, don't show this
        context.bot.send_message(chat_id=update.effective_chat.id, text=c.text['empty_list'][lang])
        return MAIN_MENU_HANDLER
    else:
        markup = ReplyKeyboardMarkup([[c.text['more'][lang]], [c.text['back'][lang]]], resize_keyboard=True, one_time_keyboard=False)
        context.bot.send_message(chat_id=update.effective_chat.id, text=f" \"{rand_quote}\" © {q_owner}", reply_markup=markup)

        return RANDOM_QUOTE_HANDLER
