from telegram import KeyboardButton, ReplyKeyboardMarkup
from models.dialogue_step import  DialogueStepModel


def get_reply_markup(step: DialogueStepModel):
    keyboard = [
        [KeyboardButton(answer.get_answer_phrase()) for answer in step.answer_options],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard)
    return reply_markup 
