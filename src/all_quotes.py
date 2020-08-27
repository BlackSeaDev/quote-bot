import config
from variables import MAIN_MENU_HANDLER
from language_set import language
from database import DB


def full_list_of_quotes(update, context):
    result = DB.getFullListOfQuotes(update.effective_chat.id)
    lang = language(update)
    if not result:
        context.bot.send_message(chat_id=update.effective_chat.id, text=config.language_config["empty_list"][lang])
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=config.language_config["all_quotes"][lang])
        for i in range(len(result)):
            context.bot.send_message(chat_id=update.effective_chat.id, text="\"{}\" © {}".format(*result[i]))

    return MAIN_MENU_HANDLER
