from telegram import ReplyKeyboardMarkup
from variables import *
import config as c

from database import DB
from os import getcwd


def language(update):
    lang = DB.getLang(update.message.chat_id)
    #print(update.effective_chat.id)
    if lang is None:
        update.message.reply_text(text=c.text['start'])
        reply_keyboard = [[c.text['ru'], c.text['en']]]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
        update.message.reply_text(text=c.text['ask_lang'], reply_markup=markup)
        return lang
    else:
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

    markup = ReplyKeyboardMarkup([[c.text['to_main_menu'][lang]]], resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text(text=c.text['thanks'][lang], reply_markup=markup)
    return MAIN_MENU_HANDLER
