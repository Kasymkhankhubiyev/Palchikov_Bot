import json
import io
from typing import NamedTuple
import random

quetions_json_file = 'questions.json'

class Question(NamedTuple):
    question: str
    answer1: str
    answer2: str
    answer3: str
    answer4: str
    true_answer: str


def load_questions() -> dict:
    """
    loads json file with questions
    """
    with io.open(quetions_json_file, encoding='utf-8-sig', mode='r') as json_file:
        questions_data = json.load(json_file)

    return questions_data


def pack_questions(questions_data: dict) -> 'dict[int, Question]':
    """
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


async def make_question():
    questions = pack_questions(load_questions())
    questions_num = len(questions.keys())
    question_id = random.randint(1, questions_num)
    message = f'Вопрос: {questions[question_id].question}\n' +\
                  f'1)  {questions[question_id].answer1}\n' +\
                  f'2)  {questions[question_id].answer2}\n' +\
                  f'3)  {questions[question_id].answer3}\n' +\
                  f'4)  {questions[question_id].answer4}\n' + 'Введите номер ответа\n для выхода введите "exit".\n'
    
    # return questions[question_id], message
    return question_id, message



def main():
    runable = True
    score = 0
    total = 0

    questions = pack_questions(load_questions())
    questions_num = len(questions.keys())

    while runable:
        question_id = random.randint(1, questions_num)
        message = f'Вопрос: {questions[question_id].question}\n' +\
                  f'1)  {questions[question_id].answer1}\n' +\
                  f'2)  {questions[question_id].answer2}\n' +\
                  f'3)  {questions[question_id].answer3}\n' +\
                  f'4)  {questions[question_id].answer4}\n' + 'Введите номер ответа\nДля выхода введите "exit"\n'
        answer = input(message)

        if answer.lower() == 'exit':
            runable = False
            print(f'\n\nYour score is {score}/{total}')
            break
        
        if answer.isdigit():
            if questions[question_id].true_answer[0] == answer:
                score += 1
                total += 1
                print('Верный ответ!')
                print(questions[question_id].true_answer + '\n\n')
            else:
                total += 1
                print('Неверный ответ!')
                print(questions[question_id].true_answer + '\n\n')
        else:
            print('нужно было ввести число')
            # print('Нужно ввести номер ответа - число! \n\n')
            # print(message)

    



if __name__=='__main__':
    main()