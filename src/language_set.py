from telegram import ReplyKeyboardMarkup
from variables import MAIN_MENU_HANDLER
import config

from database import DB
from os import getcwd


def language(update):
    lang = DB.getLang(update.message.chat_id)
    # print(update.effective_chat.id)
    if lang is None:
        update.message.reply_text(text=config.language_config['start'])
        reply_keyboard = [[config.language_config['ru'], config.language_config['en']]]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)
        update.message.reply_text(text=config.language_config['ask_lang'], reply_markup=markup)
    return lang


def setting_lang(update, context):
    answer = update.message.language_config
    if answer == config.language_config["en"]:
        lang = 1
        DB.setLang(update.effective_chat.id, lang)
    elif answer == config.language_config["ru"]:
        lang = 0
        DB.setLang(update.effective_chat.id, lang)
    else:
        # if he inputs some shit we are not allowing to go further
        return language(update)

    markup = ReplyKeyboardMarkup(
        [[config.language_config['get_random_quote'][lang], config.language_config['full_list_of_quotes'][lang]], [config.language_config['add_new_quote'][lang]]],
        resize_keyboard=True, one_time_keyboard=False)
    update.message.reply_text(text=config.language_config['thanks'][lang], reply_markup=markup)
    context.bot.send_message(chat_id=update.effective_chat.id, text=config.language_config['start_q'][lang])
    return MAIN_MENU_HANDLER
