
import config as c
from variables import MAIN_MENU_HANDLER
from language_set import language
from database import DB


def full_list_quotes(update, context):
    result = DB.getFullListQuotes(update.effective_chat.id)
    # context.bot.send_message(chat_id=update.effective_chat.id, text=f"{result[5][0]}")
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"{result}")

    # TO-DO:
    #       1. if list is empty, let user know about it
    #       2. make a message generator(loop to show all quotes one by one), if statement in this loop for q_owner == None

    return MAIN_MENU_HANDLER