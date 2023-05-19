import json
import io
from typing import NamedTuple
import random


# файл с вопросами, вариантами ответов и правильным ответом
quetions_json_file = 'questions.json'


class Question(NamedTuple):
    """
    Дата-класс для хранения данных о вопросе.

    Атрибуты:
        question, str - текстовая запись самого вопроса в виде строки
        answer1, str - текстовая запись первого варианта ответа в виде строки
        answer2, str - текстовая запись второго варианта ответа в виде строки
        answer3, str - текстовая запись третьего варианта ответа в виде строки
        answer4, str - текстовая запись четвертого варианта ответа в виде строки
        true_answer: str - текстовая запись верного ответа в формате: str(номер_верного_варианта: текстовое пояснение)
    """
    question: str
    answer1: str
    answer2: str
    answer3: str
    answer4: str
    true_answer: str


def load_questions() -> dict:
    """
    Эта функция загружает данные из json файла в словарь

    Возвращаемое значение:
        questions_data, dict - словарь с данными о вопросе
    """
    with io.open(quetions_json_file, encoding='utf-8-sig', mode='r') as json_file:
        questions_data = json.load(json_file)

    return questions_data


def pack_questions(questions_data: dict) -> 'dict[int, Question]':
    """
    Функция упаковывает данные о вопросе в список из дата-классов Question

    словарь с вопросами имеет вид:

        {'номер вопроса':{
            'Вопрос': 'str',
            'Варианты ответов': {
                '1': 'str',
                '2': 'str',
                '3': 'str',
                '4': 'str'
                },
            'Верный ответ': 'str',
            }
        }

        Аргументы:
            questions_data, dict - словарь с данными о вопросах.

        Возвращаемое значение:
            questions_dict, dict - словарь с вопросами в формате: {номер вопроса: дата-класс Question}
    """
    questions_dict = dict()
    keys = questions_data.keys()
    for key in keys:
        sub_dict = questions_data[key]
        questions_dict[int(key)] = Question(question=sub_dict['Вопрос'], 
                                       answer1=sub_dict['Варианты ответов']['1'],
                                       answer2=sub_dict['Варианты ответов']['2'],
                                       answer3=sub_dict['Варианты ответов']['3'],
                                       answer4=sub_dict['Варианты ответов']['4'],
                                       true_answer=sub_dict['Верный ответ'])
        
    return questions_dict

def prep_questions(indexes=None):
    """
    функция подготавливает вопросы и рандомно перемешанный список номеров вопросов.

    Аргументы:
        indexes, list[int] - список номер вопросов, если пустой - создаем в функции.

    Возвращаемое значение:
        questions, dict[int, Question] - словарь с вопросами
        indexes, list[int] - перемешанный список с номерами вопросов
    """

    # TODO сделать так, если index is not None - просто перемешать существуюший
    if indexes is None:
        # получаем словарь вопросов
        questions = pack_questions(load_questions())

        # получаем количество вопросов
        questions_num = len(questions.keys())

        # создаем список из последовательных номеров вопросов
        indexes = [i for i in range(1, questions_num+1, 1)]
    
    # перемешиваем рандомно индексы
    random.shuffle(indexes)

    return questions, indexes


def make_question(questions, question_id) -> str:
    """
    Функция, подготавливающая текстовое представление вопроса в формате:

        'Вопрос
        
        Вариант 1
        Вариант 2
        Вариант 3
        Вариант 4'

    Аргументы:
        questions, dict[int, Question] - словарь с вопросами
        question_id, int - ключ вопроса.

    Возвращаемое значение:
        message, str - вопрос в текстовом виде.
    """
    
    message = f'Вопрос: {questions[question_id].question}\n\n' +\
                  f'1)  {questions[question_id].answer1}\n' +\
                  f'2)  {questions[question_id].answer2}\n' +\
                  f'3)  {questions[question_id].answer3}\n' +\
                  f'4)  {questions[question_id].answer4}\n' + 'Введите номер ответа\n для выхода введите "exit".\n'
    
    # return questions[question_id], message
    return message



def main():
    """
    Функция для запуска из консоли
    """
    runable = True
    score = 0
    total = 0
    idx = 1

    questions = pack_questions(load_questions())
    questions_num = len(questions.keys())
    indexes = [i for i in range(1, questions_num+1, 1)]
    random.shuffle(indexes)

    while runable:

        if idx % questions_num == 0:
            random.shuffle(indexes)
            idx = 1
        # question_id = random.randint(1, questions_num)

        message = f'Вопрос: {questions[indexes[idx]].question}\n' +\
                  f'1)  {questions[indexes[idx]].answer1}\n' +\
                  f'2)  {questions[indexes[idx]].answer2}\n' +\
                  f'3)  {questions[indexes[idx]].answer3}\n' +\
                  f'4)  {questions[indexes[idx]].answer4}\n' + 'Введите номер ответа\nДля выхода введите "exit"\n'
        answer = input(message)

        if answer.lower() == 'exit':
            runable = False
            print(f'\n\nYour score is {score}/{total}')
            break
        
        if answer.isdigit():
            if questions[indexes[idx]].true_answer[0] == answer:
                score += 1
                print('Верный ответ!')
                print(questions[indexes[idx]].true_answer + '\n\n')
            else:
                print('Неверный ответ!')
                print(questions[indexes[idx]].true_answer + '\n\n')
            total += 1
            idx += 1
        else:
            print('нужно было ввести число')
            # print('Нужно ввести номер ответа - число! \n\n')
            # print(message)

    



if __name__=='__main__':
    main()