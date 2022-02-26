from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler
from constants import constants
from google_sheets_reader import get_dialogue_steps
from models.dialogue_step import DialogueModel

from command_handlers import start_handler, help_handler, menu_handler
from markup_helpers import get_reply_markup


def conversation_handler(update: Update, context: CallbackContext):
    dialogue = DialogueModel.instance()

    person_id = update.effective_chat.username
    message = update.effective_message.text

    next_step = dialogue.select_next_step(message, person_id)
    if next_step is None:
        update.message.reply_text(text='Ошибка, пожалуйста отправте /start и попробуйте снова')
        return
    
    reply_markup = get_reply_markup(next_step)
    reply_text = next_step.get_step_phrase()

    update.message.reply_text(text=reply_text, reply_markup=reply_markup)


if __name__ == '__main__':
    get_dialogue_steps()

    updater = Updater(constants.telegram_token)

    updater.dispatcher.add_handler(CommandHandler('start', start_handler))
    updater.dispatcher.add_handler(CommandHandler('help', help_handler))
    updater.dispatcher.add_handler(CommandHandler('menu', menu_handler))

    updater.dispatcher.add_handler(MessageHandler(None, conversation_handler))

    updater.start_polling()
    updater.idle()
