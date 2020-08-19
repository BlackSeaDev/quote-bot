from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

import config as c
from variables import MAIN_MENU_HANDLER, RANDOM_QUOTE_HANDLER
from language_set import language
from database import DB


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