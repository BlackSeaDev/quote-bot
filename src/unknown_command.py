from os import getcwd

import config
from language_set import language


def unknown_command(update, context):
    lang = language(update)
    context.bot.send_message(chat_id=update.effective_chat.id, text=config.language_config['unknown_command'][lang])
    filename = getcwd() + '/../media/photo.png'
    with open(filename, 'rb') as file:
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=file, caption=config.language_config['press_button'][lang])

