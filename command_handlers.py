from telegram import KeyboardButton, ReplyKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackContext, PicklePersistence, ConversationHandler
from constants import constants
from google_sheets_reader import get_dialogue_steps
from models.dialogue_step import DialogueModel

from markup_helpers import get_reply_markup


def start_handler(update: Update, context: CallbackContext) -> None:
    dialogue = DialogueModel.instance()

    person_id = update.effective_chat.username
    initial_step = dialogue.reset_dialogue(person_id)
    reply_markup = get_reply_markup(initial_step)
    update.message.reply_text(initial_step.phrase, reply_markup=reply_markup)


def menu_handler(update: Update, context: CallbackContext) -> None:
    dialogue = DialogueModel.instance()

    person_id = update.effective_chat.username
    menu_step = dialogue.set_last_step(person_id)
    reply_markup = get_reply_markup(menu_step)
    reply_text = menu_step.get_step_phrase()
    update.message.reply_text(reply_text, reply_markup=reply_markup)


def help_handler(update: Update, context: CallbackContext) -> None:
    help_string = "/start	Запустить бота (1 шаг)\n" \
                  "/help	Высветить все команды\n" \
                  "/menu	Доступные действия (меню из 5 шага)\n"
    update.message.reply_text(help_string)