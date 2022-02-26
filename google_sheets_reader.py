import io
import re
from math import prod
import pandas as pd
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from constants import constants
from models.dialogue_step import AnswerOptionModel, DialogueModel, DialogueStepModel
from models.product import ProductModel


_SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
_SPREADSHEET_ID = '1z0SRz-PB_DL_lCX5DoJ-4of92IqLtJadB6AU8WwpBXM'


def _get_df_from_google_sheets(sheets_service, range):
    result = sheets_service.values().get(spreadsheetId=_SPREADSHEET_ID, range=range).execute()
    values = result.get('values', [])
    csv_string = '\n'.join(['|'.join(l) for l in values])
    df = pd.read_csv(io.StringIO(csv_string), sep='|')
    return df


def get_dialogue_steps() -> DialogueModel:
    service = build('sheets', 'v4', developerKey='AIzaSyDWlsPWX_EhMH3wWbekLix65VhxTy-qi0M')
    sheet = service.spreadsheets()

    steps_df = _get_df_from_google_sheets(sheet, 'Диалог!A:D')
    products_df = _get_df_from_google_sheets(sheet, 'Товары!A:F')

    products_list = []
    for i, row in products_df.iterrows():
        products_list.append(ProductModel(int(row['Номер']), 
                                          row['Название'], 
                                          float(row['Цена с комиссией, руб']),
                                          url=row['Ссылка']
                                        ))

    dialogue = DialogueModel.instance()
    for i, row in steps_df.iterrows():
        answer_phrases_list = row['Варианты ответа'].split(';')
        answer_next_steps_list = row['Перейти на шаг'].split(';')
        answers_list = []       
        for answer_phrase, answer_next_step in zip(answer_phrases_list, answer_next_steps_list):
            answer_phrase = answer_phrase.strip()

            if re.match(r'<\S*\s?\d*>', answer_phrase) is not None:
                product_index = int(re.findall(r'\d+', answer_phrase)[0]) - 1
                if product_index < 0 or product_index >= len(products_list):
                    product_index = 0
                product = products_list[product_index]
            else:
                product = None

            answers_list.append(AnswerOptionModel(
                phrase=answer_phrase,
                step_index=int(answer_next_step),
                product=product

            ))
        dialogue_step = DialogueStepModel(
            phrase=str(row['Текст']).strip(),
            answer_options=answers_list
        )
        dialogue.add_step(dialogue_step)

    return dialogue
