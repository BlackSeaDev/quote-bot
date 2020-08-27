from telegram import ReplyKeyboardMarkup
from variables import MAIN_MENU_HANDLER
import config as c

from database import DB
from os import getcwd


def language(update):
    lang = DB.getLang(update.message.chat_id)
    # print(update.effective_chat.id)
    if lang is None:
        update.message.reply_text(text=c.text['start'])
        reply_keyboard = [[c.text['ru'], c.text['en']]]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
        update.message.reply_text(text=c.text['ask_lang'], reply_markup=markup)
    return lang


def setting_lang(update, context):
    answer = update.message.text
    if answer == c.text["en"]:
        lang = 1
        DB.setLang(update.effective_chat.id, lang)
    elif answer == c.text["ru"]:
        lang = 0
        DB.setLang(update.effective_chat.id, lang)
    else:
        # if he inputs some shit we are not allowing to go further
        return language(update)

    markup = ReplyKeyboardMarkup(
        [[c.text['get_random_quote'][lang], c.text['full_list_of_quotes'][lang]], [c.text['add_new_quote'][lang]]],
        resize_keyboard=True, one_time_keyboard=False)
    update.message.reply_text(text=c.text['thanks'][lang], reply_markup=markup)
    context.bot.send_message(chat_id=update.effective_chat.id, text=c.text['start_q'][lang])
    return MAIN_MENU_HANDLER
