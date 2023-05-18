import json
from aiogram import Bot
from aiogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import os

from tokens import token


bot = Bot(token=token)
dp = Dispatcher(bot)

async def on_startup(_):
    print('Bot is online')

############ client

b1 = KeyboardButton('/тест')
b2 = KeyboardButton('/цитатка')
b3 = KeyboardButton('/интересное')
b4 = KeyboardButton('/помощь')

main_kb = ReplyKeyboardMarkup()
main_kb.add(b1).add(b2).add(b3).add(b4)

@dp.message_handler(commands=['start', 'help', 'начать', 'помощь'])
async def command_start(message: Message):
    await bot.send_message(message.from_user.id, 'Привет! Я бот Батя-Пальчик, выучим с тобой билеты по ФОИ!', reply_markup=main_kb)


@dp.message_handler(commands=['test', 'тест'])
async def command_start_test(message: Message):
    await bot.send_message(message.from_user.id, 'Начнем тест!')


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