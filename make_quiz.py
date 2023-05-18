import json
from aiogram import Bot
from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import os

from tokens import token
from random_question_sampler import make_question, Question


class FSMAnswer(StatesGroup):
    question = State()
    answer = State()


storage = MemoryStorage()
bot = Bot(token=token)
dp = Dispatcher(bot, storage=storage)

async def on_startup(_):
    print('Bot is online')

############ client

btn_test = KeyboardButton('/тест')
btn_citation = KeyboardButton('/цитатка')
btn_intersting = KeyboardButton('/интересное')
btn_help = KeyboardButton('/помощь')


btn_1 = KeyboardButton('1')
btn_2 = KeyboardButton('2')
btn_3 = KeyboardButton('3')
btn_4 = KeyboardButton('4')
btn_end_test = KeyboardButton('закончить тест')


main_kb = ReplyKeyboardMarkup(resize_keyboard=True)
main_kb.add(btn_test).add(btn_citation).add(btn_intersting).add(btn_help)

test_kb = ReplyKeyboardMarkup(resize_keyboard=True)
test_kb.row(btn_1, btn_2).row(btn_3, btn_4).add(btn_end_test)

@dp.message_handler(commands=['start', 'help', 'начать', 'помощь'])
async def command_start(message: Message):
    await bot.send_message(message.from_user.id, 'Привет! Я бот Батя-Пальчик, выучим с тобой билеты по ФОИ!', reply_markup=main_kb)


###### pipeline тестика
@dp.message_handler(commands=['test', 'тест', 'вопрос', 'question'])
async def command_start_test(message: Message, state=None):
    await FSMAnswer.question.set()
    # await message.reply('start')
    print('next')

@dp.message_handler(state=FSMAnswer.question)
async def send_question(message: Message, state: FSMContext):
    async with state.proxy() as data:
        question = make_question()
        data['question'] = question[0]

    await FSMAnswer.next()
    print(question[1])
    await message.reply(question[1])

@dp.message_handler(state=FSMAnswer.answer)
async def catch_answer(message: Message, state: FSMContext):
    answer = 0
    print('got the answer')
    async with state.proxy() as data:
        data['answer'] = message.text

    async with state.proxy() as data:
        answer = data['answer']

    await state.finish()
    if answer != 'закончить тест':
        message.reply('Тест окончен')
    else:
        async with state.proxy() as data:
            if answer == data['question'].true_answer[0]:
                message.reply(f"Верный ответ!")
                message.reply(f"{data['question'].true_answer}")
            else:
                message.reply(f"Неверный ответ(((")
                message.reply(f"{data['question'].true_answer}")

        FSMAnswer.question.set()        


@dp.message_handler(commands=['citation', 'цитатка'])
async def command_citation(message: Message):
    await message.answer('Тут будет цитатка')


@dp.message_handler(commands=['intersting', 'интересное'])
async def command_intersting(message: Message):
    await message.answer('Что-нибудь интересненькое')


############ admin



############ basic

@dp.message_handler()
async def echo_sampler(message: Message):
    await message.answer(message.text)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
    # await message.reply(message.text)


# def main():
#     pass

# if __name__=='__main__':
#     main()