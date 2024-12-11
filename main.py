import aiogram
import logging
import asyncio
from aiogram import Dispatcher, Bot, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command


logging.basicConfig(level=logging.INFO)
TOKEN = '7252389655:AAEmtpYiwFYGALtHEZC9vpUhB0KJxV9euj0'
dp = Dispatcher()

bot = Bot(token=TOKEN)

list_student= {"Илья": "ФИО, Дата рождения, номер телефона, ЮЗ, "}

@dp.message(Command('help'))
async def start(message: types.Message, my_cakkback=None):
    await message.answer("/PRIVATE(отправляет сообщение в ЛС)"
                         " /DOX(выводит данные пользователя по типу данным)"
                         " /NETWORKS(отправляет возможные ссылки на соц сети)")

@dp.message(Command('DOX'))
async def start(message: types.Message, my_cakkback=None):
    await message.answer("выберите данные пользователя(ФИО, ДР...)")
    if

@dp.message(Command('PRIVATE'))
async def start(message: types.Message, my_cakkback=None):


@dp.message(Command('NETWORKS'))
async def start(message: types.Message, my_cakkback=None):
    await message.answer("введите данные пользователя")

async def start_dp():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(start_dp())


