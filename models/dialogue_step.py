from asyncio import current_task
from typing import List, Callable
from dataclasses import dataclass
from models.product import ProductModel


@dataclass
class AnswerOptionModel:
    def __init__(self, phrase: str, step_index: int, product: ProductModel=None) -> None:
      self.phrase = str(phrase)
      self.product = product
      self.step_index = int(step_index)
    
    def get_answer_phrase(self):
        if self.product is None:
            return self.phrase
        else:
            return f'Купил {self.product.name}'


@dataclass
class DialogueStepModel:
    def __init__(self, phrase: str, answer_options: List[AnswerOptionModel]) -> None:
        self.phrase = str(phrase)
        self.answer_options = answer_options

    def get_step_phrase(self):
        reply_text = self.phrase
        answers_products = [a.product for a in self.answer_options if a.product is not None]
        if len(answers_products) > 0:
            products_text = "\n".join([f"{i+1} - {p.name}\n{p.url}\n{p.price}RUB\n" for i, p in enumerate(answers_products)])
            reply_text = f'{reply_text}\n{products_text}'
        return reply_text


@dataclass
class DialogueModel:
    _instance = None

    _dialogue_steps_list = []
    _current_steps_per_person = {}

    def __init__(self) -> None:
        raise RuntimeError("Can't create instance of DialogueModel")

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            cls._instance._dialogue_steps_list = []
            cls._instance._current_steps_per_person = {}
        return cls._instance

    def reset_dialogue(self, person_id: str):
        self._current_steps_per_person[person_id] = 0
        return self._dialogue_steps_list[self._current_steps_per_person[person_id]]


    def add_step(self, new_step: DialogueStepModel):
        self._dialogue_steps_list.append(new_step)
    
    def get_current_step(self, person_id: str) -> DialogueStepModel:
        if person_id not in self._current_steps_per_person:
            self._current_steps_per_person[person_id] = 0
        return self._dialogue_steps_list[self._current_steps_per_person[person_id]]

    def select_next_step(self, answer_text: str, person_id: str):
        if person_id not in self._current_steps_per_person:
            self._current_steps_per_person[person_id] = 0

        current_step = self.get_current_step(person_id)
        choosen_steps_ind = [option.step_index for option in current_step.answer_options 
                             if option.get_answer_phrase() == answer_text]
        if len(choosen_steps_ind) == 0:
            return None
        else:
            next_step_index = choosen_steps_ind[0]

        if next_step_index >= len(self._dialogue_steps_list):
            next_step_index = 0

        if next_step_index == -1:
            next_step_index = self._current_steps_per_person[person_id]
        self._current_steps_per_person[person_id] = next_step_index
        return self.get_current_step(person_id)

    def set_last_step(self, person_id):
        last_step_index = len(self._dialogue_steps_list) - 1
        if person_id not in self._current_steps_per_person:
            self._current_steps_per_person[person_id] = last_step_index
        return self._dialogue_steps_list[last_step_index]
