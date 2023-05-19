"""
Это программа для подготовки к экзамену по предмету Физические Основы Информатики.

Курс читает профессор Пальчиков Евгений Иванович, Физический Факультет НГУ. 

Вопросы, цитаты, картинки и материалы взять из курса профессора.

У бота несколько основных режимов:
    1. тест - режим тестирования
    2. цитатка - интересные и веселые цитаты
    3. интересное - интересные фотографии и факты из физики и компьютерных технологий
"""


import telebot 
from telebot import types

from tokens import token
from random_question_sampler import make_question_for_bot, Question, prep_questions


bot = telebot.TeleBot(token)


# создаем основную панель с кнопками
main_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
btn_test = types.KeyboardButton('тест')
btn_citation = types.KeyboardButton('цитатка')
btn_intersting = types.KeyboardButton('интересное')
btn_help = types.KeyboardButton('помощь')
main_markup.add(btn_test, btn_citation, btn_intersting, btn_help)


# панель с кнопками для теста
question_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
btn1 = types.KeyboardButton('1')
btn2 = types.KeyboardButton('2')
btn3 = types.KeyboardButton('3')
btn4 = types.KeyboardButton('4')
btn_end_test = types.KeyboardButton('закончить тест')
question_markup.add(btn1, btn2, btn3, btn4, btn_end_test)


# хендлер старта
@bot.message_handler(content_types=['text'], commands=['start', 'help', 'начать', 'помощь', 'погнали'])
def start_help_message(message):
    bot.send_message(message.chat.id, 'Привет! Я бот <b>Батя-Пальчик</b>, выучим с тобой билеты по ФОИ!', 
                     parse_mode='html', reply_markup=main_markup)
    
    bot.register_next_step_handler(message, next_step_handler)


def next_step_handler(message):
    message_text = message.text.strip()
    if message_text in ['start', 'help', 'начать', 'помощь']:
        bot.send_message(message.chat.id, 'Привет! Я бот <b>Батя-Пальчик</b>, выучим с тобой билеты по ФОИ!', 
                     parse_mode='html', reply_markup=main_markup)
        bot.register_next_step_handler(message, next_step_handler)
    # elif message_text == 'закончить тест':
    #     bot.send_message(message.chat.id, 'Тест окончен!', 
    #                  parse_mode='html', reply_markup=main_markup)
    #     bot.register_next_step_handler(message, next_step_handler)
    elif message_text == 'тест':
        score = 0
        total = 0
        # bot.send_message(message.chat.id, 'сейчас будет тест!')
        questions, indexes = prep_questions()
        question = make_question_for_bot(questions, indexes[total])
        bot.send_message(message.chat.id, question, reply_markup=question_markup)
        bot.register_next_step_handler(message, lambda message, score=score, total=total, questions=questions, indexes=indexes: send_question(message, score, total, questions, indexes))
    elif message_text == 'цитатка':
        bot.send_message(message.chat.id, 'Вот и цитатка!')
        bot.register_next_step_handler(message, next_step_handler)
    elif message_text == 'интересное':
        bot.send_message(message.chat.id, 'Вот и цитатка!')
        bot.register_next_step_handler(message, next_step_handler)


# тут обрабатываем логику вопросиков
def send_question(message, score, total, questions, indexes):
    try:
        answer = message.text.strip()
        if answer in ['1', '2', '3', '4']:
            if answer == questions[indexes[total]].true_answer[0]:
                score += 1
                reply = '<b>Верный ответ!</b>\n'
            else:
                reply = '<b>Неверный ответ!</b>\n'
            bot.send_message(message.chat.id, reply + questions[indexes[total]].true_answer, parse_mode='html')
            total += 1
            if total != len(indexes):
                question = make_question_for_bot(questions, indexes[total])
                bot.send_message(message.chat.id, question, reply_markup=question_markup, parse_mode='html')
                bot.register_next_step_handler(message, lambda message, score=score, total=total, questions=questions, indexes=indexes: send_question(message, score, total, questions, indexes))
            else:
                reply = f'Тест окончен, вы набрали {score} из {total} = <b>{score / total * 100} %</b>.'
                bot.send_message(message.chat.id, reply, reply_markup=main_markup, parse_mode='html')
                bot.register_next_step_handler(message, next_step_handler)
        elif answer == 'закончить тест':
            reply = f'Тест окончен, вы набрали {score} из {total} = <b>{score / total * 100} %</b>.'
            bot.send_message(message.chat.id, reply, 
                        parse_mode='html', reply_markup=main_markup)
            bot.register_next_step_handler(message, next_step_handler)
        else:
            reply = 'Вы ввели что-то не то, попробуйте снова.' + make_question_for_bot(questions, indexes[total])
            question = make_question_for_bot(questions, indexes[total])
            bot.send_message(message.chat.id, question, reply_markup=question_markup, parse_mode='html')
            bot.register_next_step_handler(message, lambda message, score=score, total=total, questions=questions, indexes=indexes: send_question(message, score, total, questions, indexes))
    except:
        bot.send_message(message.chat.id, 'Ладно, я устал, пойду, полежу!\nвведи "\погнали" и мы еще поболтаем.')



@bot.message_handler(chat_types=['text'], commands=['citation', 'цитатка'])
def send_citation(message):
    bot.send_message(message.chat.id, 'Вот и цитатка!')


bot.polling(none_stop=True)
